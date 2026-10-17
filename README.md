# CampusFlow - IT Helpdesk Ticketing System

CampusFlow is a command-line application for managing IT helpdesk tickets. It helps users create, search, assign, prioritize, track, and report on tickets submitted for IT support.

## Team Members and Responsibilities

### Engineer A - Felix Gangese Terkula

Responsibilities:
- Ticket creation and validation
- Priority calculation
- Ticket storage and persistence

Main modules:
- `campusflow/tickets.py`
- `campusflow/validation.py`
- `campusflow/storage.py`

### Engineer B - Ayegba Emmanuel Onyilo

Responsibilities:
- Ticket assignment and status workflow
- Priority queue
- Reports
- Ticket search
- Ticket notes
- Engineering understanding quiz

Main modules:
- `campusflow/workflow.py`
- `campusflow/queue.py`
- `campusflow/reports.py`
- `campusflow/search.py`
- `campusflow/notes.py`
- `campusflow/quiz.py`
- `campusflow/quiz_questions.py`

## Features

- Create and validate helpdesk tickets.
- Calculate ticket priority based on urgency and affected users.
- Assign tickets to staff members.
- Update ticket statuses.
- Sort and filter tickets by priority and assignment.
- Search tickets using supported filters.
- Add and view ticket notes.
- Generate reports by category, priority, and status.
- Test understanding of the system with an engineering quiz.
- Save and load tickets using JSON storage.

## Ticket Priority Rules

Priority rules are evaluated in this order:

1. High urgency and at least 10 affected users: `critical`
2. High urgency or at least 10 affected users: `high`
3. Medium urgency or at least 3 affected users: `medium`
4. Otherwise: `low`

The critical rule must be checked before the high rule.

## Requirements

- Python 3
- Python standard library

## How to Run/Usage

1. Run `python3 main.py` from the project root.
2. Choose an option from the interactive menu.
3. Follow the prompts to create, search, assign, or update tickets.
4. Use the queue and reports options to review ticket information.
5. Use the notes options to add or view ticket notes.
6. Select the Engineering Understanding Check to test your knowledge.
7. Select Save & Exit to save tickets and close the application.

The application validates user input and reports errors for invalid
choices or unsupported operations.

## How to Run Tests

Run the complete test suite:

python3 -m unittest discover -s tests -v

## Test Status

The test suite covers ticket creation, validation, storage, status
workflows, assignment, queues, search, notes, reports, the engineering
quiz, and command-line behaviour.

Latest recorded result: 106 tests passed.

To verify the current branch, run the test command above.

## Project Structure

campusflow-next-team-A-B/
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── validation.py
│   ├── storage.py
│   ├── workflow.py
│   ├── queue.py
│   ├── reports.py
│   ├── search.py
│   ├── notes.py
│   ├── quiz.py
│   └── quiz_questions.py
├── tests/
│   ├── test_cli.py
│   ├── test_notes.py
│   ├── test_queue.py
│   ├── test_quiz.py
│   ├── test_reports.py
│   ├── test_search.py
│   ├── test_storage.py
│   ├── test_tickets.py
│   ├── test_validation.py
│   └── test_workflow.py
├── docs/
│   ├── design-decisions.md
│   ├── baseline-check.md
│   ├── ai-learning-log.md
│   └── ai-learning-log-engineer-b.md
└── README.md

## Documentation

- `docs/design-decisions.md`: Documents key design decisions and implementation rationale.
- `docs/baseline-check.md`: Records the baseline reliability audit and findings.
- `docs/ai-learning-log.md`: Shared AI learning log containing Engineer A's and Engineer B's entries.
- `docs/ai-learning-log-engineer-b.md`: Engineer B's earlier summary of AI-assisted development interactions.
