# CampusFlow - IT Helpdesk Ticketing System

CampusFlow is a command-line application for managing IT helpdesk tickets. It helps users create, search, assign, prioritize, track, and report on tickets submitted for IT support.

## Team Members and Responsibilities

### Engineer A - Felix Gangese Terkula(first team)

Responsibilities:
- Ticket creation and validation
- Priority calculation
- Ticket storage and persistence

Main modules:
- `campusflow/tickets.py`
- `campusflow/validation.py`
- `campusflow/storage.py`

### Engineer B - Onyilo

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

## How to Run

From the project root directory, run:

    python3 main.py

Follow the menu instructions to use the application.

## How to Run Tests

Run the complete test suite:

    python3 -m unittest discover -s tests -v

## Project Structure

    campusflow-next-team-A-B/
    ├── main.py
    ├── campusflow/
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
    └── docs/
        ├── design-decisions.md
        ├── ai-learning-log.md
        └── ai-learning-log-engineer-b.md

## Documentation

- `docs/design-decisions.md`: Documents key design decisions.
- `docs/ai-learning-log.md`: Engineer A's AI learning log.
- `docs/ai-learning-log-engineer-b.md`: Engineer B's AI learning log.
