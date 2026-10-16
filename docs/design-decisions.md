# CampusFlow Design Decisions

## 1. Overview

CampusFlow is a Python command-line helpdesk application
that allows a support team to manage tickets, assign staff,
track ticket status, maintain follow-up notes, organize
ticket queues, and generate reports.

This document explains the main technical decisions made
during development and the reasoning behind them.

## 2. Choice of Programming Language

### Decision

Python was used to implement CampusFlow.

### Reason

Python provides readable syntax and a built-in testing
framework. Its simplicity helps the team focus on application
logic, validation, data management, and error handling.

### Verification

The application and its automated tests are executed using
Python 3.

## 3. Modular Project Structure

### Decision

The application is divided into separate modules for
tickets, validation, workflow, notes, storage, queues,
and reports.

### Reason

Separating responsibilities makes the code easier to
understand, test, maintain, and improve.

For example:
- `tickets.py` handles ticket-related operations.
- `validation.py` contains validation logic.
- `workflow.py` handles ticket status and assignment rules.
- `notes.py` manages follow-up notes.
- `storage.py` handles JSON persistence.
- `queue.py` provides ticket queue operations.
- `reports.py` generates ticket summaries.

### Verification

The automated tests cover the different modules separately.

## 4. Input Validation

### Decision

Ticket information, staff assignments, and follow-up notes
must be validated before being accepted.

### Reason

Validation helps prevent invalid or incomplete information
from entering the application.

It also makes errors easier to detect and handle.

### Verification

Validation and related behavior are tested using the
automated test suite.

## 5. Ticket Workflow

### Decision

CampusFlow uses three ticket statuses:

- `open`
- `in_progress`
- `resolved`

The application controls which status transitions are allowed.

### Reason

Unrestricted status changes could leave tickets in
inconsistent or invalid states.

A ticket must be assigned before it can move to
`in_progress`.

A resolved ticket must be reopened before its assignment
can be changed.

### Verification

Workflow tests check permitted transitions and reject
invalid operations, including reassignment of resolved
tickets.

## 6. JSON Persistence

### Decision

JSON is used to save and load ticket data.

### Reason

JSON is a human-readable format that can represent
structured data and can be handled using Python's
standard library.

It allows ticket information to persist between
application runs.

### Verification

Storage tests check saving and loading ticket data,
including handling invalid or corrupted data.

The exact JSON structure is defined by the implementation
in `campusflow/storage.py`.

## 7. Data Integrity and Error Handling

### Decision

The application validates loaded data and detects
duplicate ticket IDs and note IDs.

A failed load should not unnecessarily damage the
existing in-memory ticket collection.

### Reason

Invalid or corrupted data could cause unexpected
application behavior or overwrite valid information.

Protecting existing data helps preserve the integrity
of the application's current state.

### Verification

Storage tests cover duplicate IDs, invalid data,
corrupted JSON, and preservation of the existing
ticket collection when loading fails.

## 8. Follow-up Notes

### Decision

Follow-up notes are validated and associated with
their corresponding tickets.

Notes cannot be added to resolved tickets.

### Reason

Notes provide a record of communication or progress
related to a support ticket.

Validation helps ensure that notes contain the
required information and are associated with
valid tickets.

### Verification

Note tests cover valid and invalid notes, note ID
ordering, and preservation of notes during storage
operations.

## 9. Automated Testing

### Decision

Python's built-in `unittest` framework is used
to test the application.

### Reason

Automated tests help verify expected behavior and
identify regressions when code changes are made.

They also provide repeatable checks for validation,
workflow rules, notes, storage, queues, and reports.

### Verification

Run the tests from the project root using:

    python3 -m unittest discover -s tests -v

Record the actual test results before submitting
changes for review.

## 10. Lessons Learned and Improvements

During development, testing helped identify areas
where the application needed stronger validation
or workflow protection.

For example, a resolved ticket must not be reassigned
until it is reopened.

This rule was reinforced through workflow testing.

Other lessons and changes should be recorded here
when they are supported by actual implementation
or test evidence.

## 11. Future Considerations

Possible future improvements include:

- Expanding automated test coverage.
- Improving error messages.
- Strengthening input validation.
- Improving data recovery and storage handling.
- Reviewing the application structure as new features
  are added.

These are potential improvements, not claims that
the features have already been implemented.