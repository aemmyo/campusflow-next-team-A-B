# CampusFlow Next Design Decisions

## 1. Overview

CampusFlow Next is a Python command-line helpdesk application that allows a support team to manage tickets, assign staff, track ticket status, maintain follow-up notes, organize ticket queues, search tickets, and generate reports.

The application also includes JSON persistence and an Engineering Understanding Check quiz.

This document explains the main technical decisions made during development and the reasons behind them.

## 2. Choice of Programming Language

### Decision

Python was used to implement CampusFlow Next.

### Reason

Python provides readable syntax and a built-in testing framework. Its simplicity allows the team to focus on application logic, validation, data management, and error handling.

### Verification

The application and its automated tests are executed using Python 3.

## 3. Modular Project Structure

### Decision

The application is divided into separate modules for tickets, validation, workflow, storage, queues, notes, search, reports, and the quiz.

### Reason

Separating responsibilities makes the code easier to understand, test, maintain, and improve.

The main modules include:

- `tickets.py`: Ticket creation and ticket-related operations.
- `validation.py`: Input validation and allowed values.
- `workflow.py`: Ticket assignment and status transitions.
- `storage.py`: JSON persistence.
- `queue.py`: Ticket queue retrieval and priority sorting.
- `notes.py`: Follow-up note management.
- `search.py`: Ticket searching and filtering.
- `reports.py`: Ticket summaries and statistics.
- `quiz.py`: Engineering Understanding Check functionality.
- `quiz_questions.py`: Quiz question data.

### Verification

Automated tests cover the application's modules and their functionality.

## 4. Ticket Priority Rules

### Decision

Ticket priority is calculated using urgency and the number of affected users.

The rules are evaluated in this order:

1. High urgency and at least 10 affected users: `critical`
2. High urgency or at least 10 affected users: `high`
3. Medium urgency or at least 3 affected users: `medium`
4. Otherwise: `low`

### Reason

The critical condition must be checked before the broader high-priority condition.

If the high-priority condition is checked first, a ticket that should receive critical priority could incorrectly be classified as high priority.

### Example

A ticket with high urgency and 12 affected users should receive critical priority.

### Verification

Ticket tests should verify the priority rules and their ordering.

## 5. Ticket ID Generation

### Decision

Generate the next ticket ID using the highest existing numeric ID rather than the number of tickets plus one.

### Reason

Counting tickets can produce duplicate IDs when tickets have been deleted or when existing tickets are loaded from storage.

Using the highest existing numeric ID helps maintain unique identifiers.

### Verification

Ticket creation and storage tests check ticket ID generation and persistence.

## 6. Input Validation

### Decision

Validate ticket information before accepting it.

Validation includes checking:

- Ticket titles are not blank.
- Categories belong to the allowed categories.
- Urgency values are valid.
- Affected-user counts are positive integers.
- Staff assignments contain valid information.
- Follow-up notes contain the required information.

### Reason

Early validation prevents invalid or incomplete data from entering the application.

It also helps the application provide meaningful error messages and handle invalid input safely.

### Verification

Validation, ticket, workflow, and notes tests cover valid inputs and common invalid values.

## 7. Ticket Data Structure

### Decision

Represent tickets as dictionaries containing fields such as:

- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

### Reason

Dictionaries provide a straightforward way to access ticket properties and work with JSON persistence.

New tickets begin with an open status and no assigned staff member.

### Verification

Ticket, workflow, and storage tests check ticket creation, updates, and persistence.

## 8. Ticket Workflow and Assignment

### Decision

Keep ticket assignment and status transitions in the workflow functionality rather than placing all business logic in the command-line interface.

The application uses three ticket statuses:

- `open`
- `in_progress`
- `resolved`

The workflow enforces permitted status transitions.

An unassigned ticket cannot move to `in_progress`. A resolved ticket must be reopened before its assignment can be changed.

### Reason

Separating workflow rules from user interaction makes the rules easier to test and reuse.

Enforcing status transitions also helps prevent tickets from entering inconsistent states.

### Verification

Workflow tests cover valid transitions, invalid transitions, assignment validation, and attempts to start work on unassigned tickets.

## 9. JSON Persistence and Error Handling

### Decision

Use JSON to save and load ticket data.

The command-line interface passes the configured data-file path to the storage functions.

A missing ticket file is handled differently from corrupted JSON or invalid saved records.

### Reason

JSON is human-readable and can be handled using Python's standard library.

It allows ticket information to persist between application runs.

Treating a missing file as a possible first application run allows the application to start with an empty ticket collection. Corrupted or invalid saved data should produce an appropriate error instead of being silently treated as an empty collection.

### Data Integrity

The application validates loaded data and checks for duplicate ticket IDs and note IDs.

A failed load should not unnecessarily damage the existing in-memory ticket collection.

### Verification

Storage tests cover saving, loading, malformed JSON, duplicate IDs, invalid stored records, and error handling.

## 10. Ticket Queues

### Decision

Provide separate functions for retrieving open tickets, retrieving tickets assigned to staff, and sorting tickets by priority.

### Reason

These operations help users identify outstanding work and organize tickets for follow-up.

Keeping queue operations separate from the CLI also makes them easier to test.

Sorting results should not unexpectedly modify the original ticket collection.

### Verification

Queue tests cover retrieval, staff-name matching, priority sorting, and preservation of the original list.

## 11. Ticket Search and Filtering

### Decision

Keep search functionality in a dedicated search module.

Users can search ticket titles and filter results using supported criteria, including category, status, and priority.

Search filters can be combined, and matching is case-insensitive where applicable.

Search results can also be sorted by priority.

### Reason

Separating search logic from the CLI allows filtering rules to be tested independently of user input and display code.

### Verification

Search tests cover individual filters, combined filters, case-insensitive title matching, invalid filters, empty results, and sorting.

## 12. Follow-up Notes

### Decision

Manage ticket notes through dedicated note-management functions rather than mixing note operations with ticket creation and workflow logic.

Notes are associated with their corresponding tickets and validated before being accepted.

### Reason

Follow-up notes provide a record of communication or progress related to a support ticket.

Separating note management keeps note validation and retrieval independent of other ticket operations.

### Verification

Notes tests cover validation, note retrieval, note IDs, and note behavior when ticket status changes.

Storage tests should also verify that notes are preserved when ticket data is saved and loaded.

## 13. Reports and Analytics

### Decision

Use dedicated reporting functions to calculate ticket summaries and counts by status, priority, category, and assignment.

### Reason

Centralizing these calculations avoids duplicating reporting logic throughout the CLI and makes the results easier to test.

Reports help users understand ticket activity and identify outstanding work.

### Verification

Report tests cover totals, category counts, priority counts, status counts, assignment statistics, and resolution statistics where implemented.

## 14. Engineering Understanding Check

### Decision

Provide the Engineering Understanding Check as a separate quiz module, with quiz questions maintained in a dedicated question module.

### Reason

Separating quiz execution from question data makes the quiz easier to maintain and test.

The quiz allows users to answer questions and receive a score after completing the assessment.

### Verification

Quiz tests cover correct and incorrect answers, empty answers, case-insensitive answer handling, and score calculation.

## 15. Command-Line Interface

### Decision

Use `main.py` to connect the application's features through a menu-driven command-line interface.

The menu provides access to ticket management, assignment, status updates, queues, reports, search, notes, the Engineering Understanding Check, and saving and exiting.

### Reason

A menu-driven interface makes the application's functionality accessible without requiring users to call Python functions directly.

Input validation and error handling help the application respond appropriately to invalid choices and operational errors.

### Verification

CLI tests cover invalid menu choices and saving and exiting. Manual testing can also be used to check user interactions.

## 16. Automated Testing

### Decision

Use Python's built-in `unittest` framework to test individual modules and the integrated application.

### Reason

Automated tests help identify regressions when code changes are made or features are combined.

They provide repeatable checks for ticket management, validation, workflow, storage, queues, search, notes, reports, quizzes, and CLI behavior.

### Verification

Run the test suite from the project root using:

    python3 -m unittest discover -s tests -v

During the current merge work, a test run completed with 111 tests passing and no failures or errors.

The application should be tested again after all merge conflicts have been resolved so the recorded result reflects the final integrated version.

## 17. Lessons Learned

The project reinforced several engineering practices:

- Check specific conditions before broader conditions when rule ordering affects results.
- Generate identifiers from existing data rather than assuming the number of records determines the next ID.
- Distinguish missing files from corrupted saved data.
- Validate input before modifying application data.
- Separate business logic into modules that can be tested independently.
- Protect existing data when loading new data fails.
- Test successful operations and failure conditions.
- Verify feature integration as well as individual functions.
- Review AI-generated suggestions through code inspection and automated testing.

## 18. Future Considerations

Possible future improvements include:

- Expanding automated test coverage.
- Improving error messages.
- Strengthening input validation.
- Improving data recovery and storage handling.
- Reviewing the application structure as new features are added.
- Adding further tests for edge cases and integration behavior.

These are potential improvements and should not be interpreted as features that have already been implemented.