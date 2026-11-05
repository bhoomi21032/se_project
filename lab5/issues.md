# Issues: helpdesk_system.py

Line numbers refer to the ORIGINAL file. Ordered by severity.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell injection via `shell=True` (Bandit B602, High) | Security | 38 | `"ping -c 1 " + hostname` run through the shell, so `x; rm -rf /` executes. | Validate hostname with a regex, call `subprocess.call([ping, "-c", "1", host])` with no shell. |
| Hardcoded admin password (Bandit B105) | Security | 8, 54 | Password sits in source and is repeated in `main()`. | Read from `HELPDESK_ADMIN_PASSWORD` env var; compare with `hmac.compare_digest`. |
| Mutable default argument (Pylint W0102) | Bug | 10 | `audit_trail=[]` is shared across calls, so the audit log leaks between callers. | Default to `None`, create a new list inside. |
| No urgency validation (logic bug, no tool flags it) | Bug | 13, 49 | `-7` and `99` are accepted; `abc` crashes with an uncaught `ValueError`. | `parse_priority()` enforces 1-5; `main()` catches `ValueError` and prints a message. |
| Bare `except: pass` (Pylint W0702, Flake8 E722, Bandit B110) | Bug | 22-24 | Swallows every error, so `add_note(999, ...)` silently does nothing. | Check `ticket_id in tickets`, return `False` if missing. |
| `close_ticket` fails silently / `KeyError` | Bug | 26-28 | Wrong password does nothing, unknown id raises `KeyError`. | Return `bool`; use `tickets.pop(id, None)`. |
| Global counter (Pylint W0603, C0103) | Design | 7, 11 | `global ticket_counter` and non-constant naming. | `itertools.count(101)` and `next()`. |
| File not closed safely (Pylint R1732, W1514) | Bug | 41-43 | `open()` without `with` or encoding; file leaks on error. | `with open(..., encoding="utf-8")` and `json.dump`. |
| `== None` (Pylint C0121, Flake8 E711) | Style | 33 | Should use identity check. | `is None`. |
| `unresolvedHighPriority` naming (Pylint C0103) | Style | 30 | Not snake_case. | Rename `unresolved_high_priority`; iterate with `.items()` (C0206). |
| Magic numbers | Style | 33 | `4` and `100`/`1-5` unexplained. | Named constants. |
| Missing docstrings (C0114, C0116) | Style | all | No module or function docs. | Add docstrings. |
| Unused variable `t2` (W0612, F841) | Style | 47 | Assigned, never used. | Drop the assignment. |
| `%` formatting (C0209) | Style | 14 | Old string formatting. | f-string. |
| Long lines / blank lines (E501, E302, E305) | Style | 13, 14, 52, defs | PEP 8 violations. | Wrap lines; 2 blank lines between defs. |
| `main()` runs on import | Design | 58 | Importing the module runs the demo. | `if __name__ == "__main__":` guard. |
| `import subprocess` (Bandit B404) | Security (info) | 2 | Informational. | `# nosec B404` with justification, after the real fix above. |

**Before / after**

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.53/10 (20 messages) | 10.00/10 |
| Bandit | 4 issues (1 High, 3 Low) | 0 |
| Flake8 | 15 issues | 0 |
