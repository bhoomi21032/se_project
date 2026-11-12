# LAB7 - Fuzzing with Hypothesis

Setup (VS Code terminal, inside LAB7):
    pip install -r requirements.txt

BEFORE (buggy) - screenshots for Steps 2 and 4:
    cd before
    python processor.py            # enter: EARLY  (no dash) -> crashes
    python -m pytest test_processor.py   # tests FAIL
    cd ..

AFTER (fixed) - screenshots for Steps 5 and 6:
    python processor.py            # try: early-20 / vip@4 / Asha,17,A12 / bad inputs
    python -m pytest test_processor.py   # 7 passed

Submit: processor.py (fixed), test_processor.py, PDF of screenshots.
