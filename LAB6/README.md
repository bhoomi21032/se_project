# Lab 6 - Event Ticket Tier
pip install coverage pytest

Line coverage:
  coverage run -m pytest CodeCoverageTest_xxxx_application.py
  coverage report -m

Branch coverage:
  coverage erase
  coverage run --branch -m pytest BranchCoverageTest_xxxx_application.py
  coverage report -m
