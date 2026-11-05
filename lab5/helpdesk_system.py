"""IT helpdesk ticket allocator.

Raises tickets with an urgency level, assigns technicians, records notes,
lists unassigned high-priority tickets and saves everything to JSON.
"""
import hmac
import itertools
import json
import os
import re
import shutil
# Only used with a validated hostname (see ping_user_machine)
import subprocess  # nosec B404
from datetime import datetime

MIN_PRIORITY = 1
MAX_PRIORITY = 5
DEFAULT_PRIORITY = 3
HIGH_PRIORITY = 4
HOSTNAME_PATTERN = re.compile(
    r"^[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?$"
)

tickets = {}
ticket_ids = itertools.count(101)


def get_admin_password():
    """Read the admin password from the environment, never from source."""
    return os.environ.get("HELPDESK_ADMIN_PASSWORD", "")


def parse_priority(urgency):
    """Convert urgency to an int and make sure it is within 1-5."""
    priority = int(urgency)
    if not MIN_PRIORITY <= priority <= MAX_PRIORITY:
        raise ValueError(
            f"urgency must be {MIN_PRIORITY}-{MAX_PRIORITY}, got {priority}"
        )
    return priority


def raise_ticket(user, issue_type, urgency=str(DEFAULT_PRIORITY),
                 audit_trail=None):
    """Create a ticket and return its id. Raises ValueError on bad urgency."""
    if audit_trail is None:
        audit_trail = []
    priority = parse_priority(urgency)
    ticket_id = next(ticket_ids)
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }
    audit_trail.append(f"{user} raised #{ticket_id} at {datetime.now()}")
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign a technician to an existing ticket."""
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to a ticket. Returns False if the ticket does not exist."""
    if ticket_id not in tickets:
        return False
    tickets[ticket_id]["notes"].append(note)
    return True


def close_ticket(ticket_id, password):
    """Delete a ticket if the admin password is right and the ticket exists."""
    expected = get_admin_password()
    if not expected or not hmac.compare_digest(password, expected):
        return False
    return tickets.pop(ticket_id, None) is not None


def unresolved_high_priority():
    """Return ids of high-priority tickets that have no technician."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= HIGH_PRIORITY and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Ping a host once. Rejects anything that is not a plain hostname/IP."""
    if not HOSTNAME_PATTERN.match(hostname):
        raise ValueError(f"invalid hostname: {hostname!r}")
    ping = shutil.which("ping")
    if ping is None:
        raise FileNotFoundError("ping executable not found")
    # list args + shell=False + validated input, so no shell injection
    return subprocess.call([ping, "-c", "1", hostname])  # nosec B603


def save_tickets(file="tickets.json"):
    """Write all tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(tickets, handle)


def main():
    """Demo run."""
    t1 = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    try:
        raise_ticket("joe", "vpn", "-7")
    except ValueError as err:
        print("Rejected ticket:", err)
    t3 = raise_ticket("joe", "vpn", "2")
    assign_ticket(t1, "Tech-Kiran")
    if not add_note(999, "Called user"):
        print("Note not added: ticket 999 does not exist")
    print("Unassigned high priority:", unresolved_high_priority())
    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ")
    try:
        raise_ticket("sana", "laptop", level or str(DEFAULT_PRIORITY))
    except ValueError as err:
        print("Rejected ticket:", err)
    if not close_ticket(t3, os.environ.get("HELPDESK_ADMIN_PASSWORD", "")):
        print("Ticket not closed (set HELPDESK_ADMIN_PASSWORD)")
    save_tickets()
    print("Open tickets:", list(tickets))


if __name__ == "__main__":
    main()
