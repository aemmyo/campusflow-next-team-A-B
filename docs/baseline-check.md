# CampusFlow Next Baseline Check

## 1. Project Overview

CampusFlow Next is a Python command-line helpdesk application designed to manage support tickets.

The application supports:
- Ticket creation and validation
- Ticket assignment and priority calculation
- Ticket status changes and workflow safety
- Follow-up notes
- Ticket queues and priority sorting
- Search and filtering
- Reports and analytics
- JSON storage and data persistence
- The Engineering Understanding Check quiz

This document records the baseline assessment, the problems identified, and the verification performed during development.

## 2. Baseline Information

- Baseline commit: `0519c17`
- Commit message: Fix resolved ticket assignment safety
- Baseline branch: `main`
- Environment: Python 3
- Audit method: The baseline was extracted into `/tmp` using `git archive`, without changing the feature branch.

## 3. Initial Baseline Test Results

Command:

`python3 -m unittest discover -s tests -v`

Observed results:
- Tests run: 85
- Passed: 85
- Failures: 0
- Errors: 0
- Final result: `OK`

All 85 tests passed at baseline commit `0519c17`.

However, passing the unit tests did not establish that the application could start successfully through its normal command-line entry point.

## 4. Baseline CLI Startup Check

Command:

`python3 main.py`

Expected result:

The application should start and display the interactive menu.

Actual result:

The application crashed before displaying the menu.

Error:

`TypeError: load_tickets() missing 1 required positional argument: 'path'`

Cause:

The baseline CLI called `load_tickets()` without an argument, while `campusflow/storage.py` defines the function as `load_tickets(path)`.

Impact:

The application could not start through its normal entry point.

## 5. Baseline Save-Function Inspection

The baseline CLI called:

`save_tickets(tickets)`

However, the storage function requires two arguments:

`save_tickets(tickets, path)`

Finding:

The CLI omitted the required storage path argument.

Limitation:

This issue was identified by inspecting the source code. The save operation was not executed because the application crashed during startup.

## 6. Three Baseline Audit Checks

### Check 1: Automated Tests

- Initial state: Baseline commit `0519c17`
- Command: `python3 -m unittest discover -s tests -v`
- Expected: The baseline test suite should execute and report its results.
- Actual: All 85 tests passed with no failures or errors.

### Check 2: CLI Startup

- Initial state: Baseline commit `0519c17`
- Command: `python3 main.py`
- Expected: The interactive menu should appear.
- Actual: Startup failed because `load_tickets()` was called without its required path argument.

### Check 3: Save-Function Compatibility

- Initial state: Baseline source at commit `0519c17`
- Method: Inspected the CLI call and storage function definition.
- Expected: The CLI should supply all required arguments.
- Actual: The CLI supplied only `tickets`, while the function requires both `tickets` and `path`.
- Limitation: This was a source-code inspection, not a successful runtime test of the save operation.

## 7. Problems Identified and Improvements

The project was reviewed for weaknesses in ticket safety, validation, workflow management, and data persistence.

Important areas include:

- Validation of ticket assignments.
- Prevention of reassignment while a ticket is resolved.
- Enforcement of permitted status transitions.
- Prevention of unassigned tickets entering `in_progress`.
- Validation of follow-up notes.
- Detection of duplicate ticket IDs and note IDs.
- Rejection of invalid or corrupted JSON data.
- Preservation of existing ticket data when loading fails.
- Correct use of required arguments in storage function calls.

These areas should be verified through the relevant implementation and automated tests.

## 8. Current-Branch Verification

During the merge work for the `feature/engineer-a-ticket-safety` branch, the following command was used to run the complete test suite:

`python3 -m unittest discover -s tests -v`

The observed result was:

- Tests run: 111
- Passed: 111
- Failures: 0
- Errors: 0
- Final result: `OK`

The `main.py` file also passed a Python syntax check using:

`python3 -m py_compile main.py`

These results establish that the application passed the reported test suite and syntax check at that point in development.

The results should be checked again after all merge conflicts are resolved, because further changes may affect the application.

## 9. Remaining Audit Needs

The following areas should be checked against the project requirements:

- Whether invalid ticket categories are rejected.
- Whether search and filtering meet the assessment requirements.
- Whether reports handle required analytics and edge cases.
- Whether quiz scoring and invalid CLI choices are tested.
- Whether required documentation and learning logs are complete.
- Whether both engineers have completed their assigned pull requests and peer reviews.

Untested behaviour should not be reported as a confirmed defect.

## 10. Lessons Learned

The baseline assessment demonstrates the importance of:

- Running tests and checking application startup separately.
- Supplying all required function arguments.
- Validating user input before changing application data.
- Enforcing workflow rules in application logic.
- Testing both successful operations and failure conditions.
- Protecting existing data when loading new data fails.
- Distinguishing observed results from assumptions.
- Reviewing AI-generated suggestions and verifying them against the actual code.

## 11. Conclusion

At baseline commit `0519c17`, all 85 unit tests passed, but the CLI could not start because the storage function was called without its required path argument.

During subsequent development, the complete test suite was reported to pass 111 tests, and `main.py` passed its syntax check.

The test suite must be run again after resolving the remaining merge conflicts to confirm the final integrated version of CampusFlow Next.
