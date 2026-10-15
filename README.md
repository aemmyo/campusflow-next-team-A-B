# CampusFlow

CampusFlow is a Python command-line helpdesk application
for managing support tickets.

It helps a support team create tickets, assign staff, track
ticket status, manage follow-up notes, organize ticket queues,
and generate reports.

The application uses JSON storage to preserve ticket data
between program runs.

## Features

### Ticket Management
- Create support tickets.
- Validate ticket information.
- Calculate ticket priority.
- Assign tickets to staff members.
- Track ticket status.
- Reopen resolved tickets when necessary.
- Enforce valid status transitions.

### Ticket Safety
- Reject invalid ticket information.
- Reject blank staff assignments.
- Prevent reassignment of resolved tickets until they are reopened.
- Prevent unassigned tickets from moving to in-progress status.
- Reject invalid status transitions.

### Follow-up Notes
- Add follow-up notes to tickets.
- Validate note content and author information.
- Prevent notes from being added to resolved tickets.
- Preserve existing notes when tickets are saved and loaded.
- Maintain note ID ordering.

### Data Storage
- Save tickets and notes to JSON.
- Load previously saved ticket data.
- Validate loaded ticket information.
- Detect duplicate ticket IDs and note IDs.
- Reject corrupted or invalid JSON data.
- Preserve the existing ticket collection when loading fails.

### Ticket Queues
- Retrieve open tickets.
- Retrieve tickets assigned to a staff member.
- Sort tickets by priority.
- Support case-insensitive staff-name matching.

### Reports
- Count tickets.
- Group tickets by status.
- Group tickets by priority.
- Group tickets by category.
- Count assigned and unassigned tickets.

### Search and Other Features
[Document the search, CLI, quiz, or other features actually
implemented by the team.]

## Requirements

- Python 3
- A terminal or command-line interface
- Git, if you want to clone the repository

## Installation

Clone the repository:

    git clone https://github.com/aemmyo/campusflow-next-team-A-B.git

Enter the project directory:

    cd campusflow-next-team-A-B

## Running the Application

Run the application from the project root:

    python3 main.py

Follow the prompts displayed by the application.

Note: The available commands and prompts depend on the
features implemented in the current version.

## Running the Tests

Run the complete automated test suite:

    python3 -m unittest discover -s tests -v

The latest verified test run completed with:

    Ran 85 tests
    OK

The test suite covers ticket management, validation,
notes, storage, queues, reports, and workflow behavior.

Run the tests again after making code changes.

## Project Structure

    campusflow-next-team-A-B/
    |
    |-- campusflow/
    |   |-- __init__.py
    |   |-- notes.py
    |   |-- queue.py
    |   |-- reports.py
    |   |-- storage.py
    |   |-- tickets.py
    |   |-- validation.py
    |   |-- workflow.py
    |
    |-- tests/
    |   |-- __init__.py
    |   |-- test_notes.py
    |   |-- test_queue.py
    |   |-- test_reports.py
    |   |-- test_storage.py
    |   |-- test_tickets.py
    |   |-- test_validation.py
    |   |-- test_workflow.py
    |
    |-- docs/
    |   |-- baseline-check.md
    |   |-- ai-learning-log.md
    |
    |-- main.py
    |-- README.md

## JSON Persistence

CampusFlow uses JSON to store ticket information.

The storage module is responsible for saving and loading
ticket data.

Stored information should be validated before it is accepted
into the application's ticket collection.

Invalid or corrupted data should be rejected without
unnecessarily damaging the existing in-memory collection.

The exact JSON structure should match the implementation
in `campusflow/storage.py`.

## Ticket Workflow

The application supports the following ticket statuses:

- `open`
- `in_progress`
- `resolved`

Permitted transitions are:

- `open` to `in_progress`
- `in_progress` to `open`
- `in_progress` to `resolved`
- `resolved` to `open`

A ticket must be assigned before it can move to
`in_progress`.

A resolved ticket must be reopened before its assignment
can be changed.

## Development and Testing

The project uses Python's built-in `unittest` framework.

Tests verify expected behavior and error handling across
ticket management, workflow transitions, notes, validation,
queues, reports, and JSON persistence.

Before submitting changes, run:

    python3 -m unittest discover -s tests -v

## Team Contributions

### Engineer A — Ticket Safety and Storage

Responsible for:
- Validation helpers.
- Ticket assignment and status safety.
- Follow-up note validation.
- JSON persistence and data validation.
- Duplicate ticket and note ID protection.
- Protecting existing ticket collections when loading fails.
- Relevant automated tests.

### Engineer B — Search, Reports, and CLI

Responsible for:
- Ticket search.
- Reporting functionality.
- Command-line interactions.
- Quiz or understanding-check functionality, if implemented.
- Relevant automated tests and documentation.

Update these descriptions if the team's final responsibilities
or implementation differ.

## Documentation

Additional project documentation is available in `docs/`:

- `design-decisions.md` records the project baseline, observed
  issues, and verification results.
- `ai-learning-log.md` records AI-assisted learning,
  verification, and engineering decisions.

## Future Improvements

Possible future improvements include:
- More comprehensive input validation.
- Additional automated tests.
- Improved command-line usability.
- More reporting and search options.
- Improved error messages.
- Further testing of invalid and unexpected input.
