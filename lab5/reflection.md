# Reflection

> The handout text I could extract did not list the four questions explicitly. These are the standard ones for this lab; swap in the exact wording from your copy if it differs.

**1. Which issues were easiest and hardest to fix?**
Easiest: style ones (`== None`, blank lines, unused variable, f-strings), mostly mechanical. Hardest: the `shell=True` ping. Removing the shell is one line, but proving the input is safe needed hostname validation, and Bandit still reports `subprocess` imports and calls at Low, so those needed a justified `# nosec`.

**2. Did the tools give false positives or miss anything?**
B404 (importing `subprocess`) is noise on its own, and B105 would flag any string that looks like a password. More important were the misses: none of the three tools flagged that urgency `-7` or `99` is accepted, that `abc` crashes the program, or that `close_ticket` silently ignores a wrong password. Running the program and reading its output caught those.

**3. How would you integrate static analysis into a workflow?**
Run flake8 and pylint as a pre-commit hook and in CI on every pull request, with Bandit as a separate security job that fails the build on Medium or High. Set a minimum Pylint score and keep a config file so the team shares the same rules.

**4. What tangible improvements did you see?**
Pylint went from 5.53 to 10.00, Bandit from 1 High and 3 Low to 0, Flake8 from 15 issues to 0. Beyond scores: no shell injection, no hardcoded secret, no shared mutable audit list, errors reported instead of swallowed, and the module is safe to import and test.
