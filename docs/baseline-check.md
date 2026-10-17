# CampusFlow Baseline Check

## 1. Baseline Information

- Baseline commit: `0519c17`
- Commit message: Fix resolved ticket assignment safety
- Baseline branch: main
- Environment: Python 3
- Audit method: Extracted the baseline into `/tmp` using `git archive`, without changing the current feature branch.

## 2. Baseline Test Results

Command: `python3 -m unittest discover -s tests -v`

Observed results:
- Tests run: 85
- Passed: 85
- Failures: 0
- Errors: 0
- Final result: OK

All 85 tests passed at baseline commit `0519c17`.

## 3. CLI Startup Check

Command: `python3 main.py`

Expected: The application should display the interactive menu.

Actual: The application crashed before displaying the menu.

Error:
`TypeError: load_tickets() missing 1 required positional argument: 'path'`

Cause: The baseline CLI called `load_tickets()` without an argument, but `campusflow/storage.py` defines `load_tickets(path)`.

Impact: The CLI could not start through its normal entry point.

## 4. CLI Save-Call Inspection

The baseline CLI called `save_tickets(tickets)`, but the storage function is defined as `save_tickets(tickets, path)`.

Finding: The CLI omitted the required path argument.

Limitation: This was confirmed by inspecting the source code. The save operation was not executed because the application crashed during startup.

## 5. Three Baseline Audit Checks

### Check 1: Unit tests

- Initial state: Baseline commit `0519c17`.
- Command: `python3 -m unittest discover -s tests -v`
- Expected: The baseline test suite should execute and report its results.
- Actual: 85 tests passed with no failures or errors.

### Check 2: CLI startup

- Initial state: Baseline commit `0519c17`.
- Command: `python3 main.py`
- Expected: The interactive menu should appear.
- Actual: Startup failed because `load_tickets()` was called without its required path argument.

### Check 3: Save-function compatibility

- Initial state: Baseline source at commit `0519c17`.
- Method: Inspected the CLI call and storage function definition.
- Expected: The CLI should supply all required arguments.
- Actual: The CLI passed only `tickets`, while the function requires `tickets` and `path`.
- Limitation: This was source-code inspection, not a successful runtime test of the save operation.

## 6. Current-Branch Comparison

Current branch: `feat/integrate-search-insights`

The current CLI calls:
- `load_tickets(DATA_FILE)`
- `save_tickets(tickets, DATA_FILE)`

These calls supply the required path argument.

Command: `python3 -m unittest tests.test_cli -v`

Observed results:
- `test_invalid_menu_choice`: passed
- `test_save_and_exit`: passed
- Tests run: 2
- Failures: 0
- Errors: 0

## 7. Remaining Audit Needs

The baseline test suite passed, but the CLI could not start because of the missing storage path argument.

The current branch supplies the required path and has two passing CLI tests.

The following areas need separate verification:
- Whether the baseline accepts an invalid category such as `access`.
- Whether search and filtering meet all assessment requirements.
- Whether reports meet all required analytics and edge cases.
- Whether both engineers have completed the required pull requests and peer reviews.

Untested behavior is not recorded as a confirmed defect.
