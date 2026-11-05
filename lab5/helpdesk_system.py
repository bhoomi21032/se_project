import json
import os
import re
import shutil
import subprocess  # nosec B404
from datetime import datetime

# Global state
tickets = {}
ticket_counter = 100
HOSTNAME_PATTERN = re.compile(r"^[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?$")

def get_admin_password():
    return os.environ.get("HELPDESK_ADMIN_PASSWORD", "")

def raise_ticket(user, issue_type, urgency="3", audit_trail=[]):
    global ticket_counter
    ticket_counter += 1
    tickets[ticket_counter] = {"user": user, "issue": issue_type, "priority": int(urgency), "tech": None, "notes": []}
    audit_trail.append("%s raised #%d at %s" % (user, ticket_counter, datetime.now()))
    return ticket_counter

def assign_ticket(ticket_id, technician):
    tickets[ticket_id]["tech"] = technician

def add_note(ticket_id, note):
    if ticket_id in tickets:
        tickets[ticket_id]["notes"].append(note)

def close_ticket(ticket_id, password):
    if password == get_admin_password():
        del tickets[ticket_id]

def unresolvedHighPriority():
    result = []
    for t in tickets:
        if tickets[t]["priority"] >= 4 and tickets[t]["tech"] == None:
            result.append(t)
    return result

def ping_user_machine(hostname):
    if not HOSTNAME_PATTERN.match(hostname):
        raise ValueError("invalid hostname")
    ping = shutil.which("ping")
    return subprocess.call([ping, "-c", "1", hostname])  # nosec B603

def save_tickets(file="tickets.json"):
    f = open(file, "w")
    f.write(json.dumps(tickets))
    f.close()

def main():
    t1 = raise_ticket("anil", "printer", "5")
    t2 = raise_ticket("meera", "wifi", "4")
    t3 = raise_ticket("joe", "vpn", "-7")
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolvedHighPriority())
    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ") or "3"
    raise_ticket("sana", "laptop", level)
    close_ticket(t3, get_admin_password())
    save_tickets()
    print("Open tickets:", list(tickets.keys()))

main()
