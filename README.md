# CampusFlow

## Team

- Engineer A:Adama shalom. Ticket validation, workflow safety, notes, and storage.

CampusFlow is a Python command-line helpdesk application for managing support tickets.

It helps a support team create tickets, assign staff, track ticket status, manage follow-up notes, organize ticket queues, and generate reports.

The application uses JSON storage to preserve ticket data between program runs.

## Features

### 1. Ticket Management

- Create support tickets.
- Validate ticket information.
- Calculate ticket priority.
- Assign tickets to staff members.
- Track ticket status.
- Reopen resolved tickets when necessary.
- Enforce valid status transitions.

### 2. Ticket Safety

- Reject invalid ticket information.
- Reject blank staff assignments.
- Prevent reassignment of resolved tickets until they are reopened.
- Prevent unassigned tickets from moving to `in_progress`.
- Reject invalid status transitions.

### 3. Follow-up Notes

- Add follow-up notes to tickets.
- Validate note content and author information.
- Prevent notes from being added to resolved tickets.
- Preserve existing notes when tickets are saved and loaded.
- Maintain note ID ordering.

### 4. Data Storage

- Save tickets and notes to JSON.
- Load previously saved ticket data.
- Validate loaded ticket information.
- Detect duplicate ticket IDs and note IDs.
- Reject corrupted or invalid JSON data.
- Preserve the existing ticket collection when loading fails.

### 5. Ticket Queues

- Retrieve open tickets.
- Retrieve tickets assigned to a staff member.
- Sort tickets by priority.
- Support case-insensitive staff-name matching.

### 6. Reports

- Count tickets.
- Group tickets by status.
- Group tickets by priority.
- Group tickets by category.
- Count assigned and unassigned tickets.

### 7. Search and Other Features

Search, command-line interactions, quizzes, and other additional features should be documented here only when they are implemented in the current project version.

## Requirements

- Python 3
- A terminal or command-line interface
- Git, if you want to clone the repository

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aemmyo/campusflow-next-team-A-B.git
```

### 2. Enter the project directory

```bash
cd campusflow-next-team-A-B
```

## Running the Application

From the project root, run:

```bash
python3 main.py
```

Follow the prompts displayed by the application.

The available commands and prompts depend on the features implemented in the current version.

## Running the Tests

CampusFlow uses Python's built-in `unittest` framework.

Run the complete test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The latest verified test run completed with:

```text
Ran 86 tests
OK
```

The test suite covers ticket management, validation, notes, storage, queues, reports, and workflow behavior.

Run the tests again after making code changes to check that existing functionality continues to work.

## Project Structure

The main project files are organized as follows:

```text
campusflow-next-team-A-B/
├── campusflow/
│   ├── __init__.py
│   ├── notes.py
│   ├── queue.py
│   ├── reports.py
│   ├── storage.py
│   ├── tickets.py
│   ├── validation.py
│   └── workflow.py
├── tests/
│   ├── __init__.py
│   ├── test_notes.py
│   ├── test_queue.py
│   ├── test_reports.py
│   ├── test_storage.py
│   ├── test_tickets.py
│   ├── test_validation.py
│   └── test_workflow.py
├── docs/
│   ├── baseline-check.md
│   ├── ai-learning-log.md
│   └── design-decisions.md
├── main.py
└── README.md
```

This structure describes the known project layout. If the repository contains additional files, update the tree to reflect the actual structure.

## JSON Persistence

CampusFlow uses JSON to store ticket information between program runs.

The storage module is responsible for saving and loading ticket data.

Stored information must be validated before it is accepted into the application's ticket collection.

Invalid or corrupted data should be rejected without unnecessarily damaging the existing in-memory collection.

The exact JSON structure and storage behavior are defined by the implementation in `campusflow/storage.py`.

## Ticket Workflow

The application supports the following ticket statuses:

- `open`
- `in_progress`
- `resolved`

The permitted status transitions are:

- `open` to `in_progress`
- `in_progress` to `open`
- `in_progress` to `resolved`
- `resolved` to `open`

A ticket must be assigned before it can move to `in_progress`.

A resolved ticket must be reopened before its assignment can be changed.

These rules help maintain consistent ticket state and prevent invalid workflow operations.

## Development and Testing

Before submitting code changes, run the automated tests:

```bash
python3 -m unittest discover -s tests -v
```

The tests verify expected behavior and error handling across ticket management, workflow transitions, notes, validation, queues, reports, and JSON persistence.

New functionality should include appropriate automated tests.

## Team Contributions

### Engineer A — Ticket Safety and Storage

Responsibilities include:

- Implementing validation helpers.
- Enforcing ticket assignment and status safety.
- Validating follow-up notes.
- Implementing JSON persistence and data validation.
- Preventing duplicate ticket and note IDs.
- Preserving existing ticket collections when loading fails.
- Writing and maintaining relevant automated tests.
