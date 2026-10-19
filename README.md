# CampusFlow Next - IT Helpdesk Ticketing System

CampusFlow Next is an updated Python command-line application for managing IT helpdesk tickets.

The application allows users to create, validate, assign, prioritize, search, and track support tickets. It also supports ticket notes, priority queues, reports, JSON storage, and an Engineering Understanding Check quiz.

The project emphasizes reliable data handling, input validation, safe ticket workflows, modular design, and automated testing.

## Team Members and Responsibilities

### Engineer A - Adama Shalom

Responsibilities:
- Ticket validation and safety
- Workflow safety and valid status transitions
- Ticket notes
- Reliable ticket storage and data validation

### Engineer B - Ayegba Emmanuel Onyilo

Responsibilities:
- Ticket assignment and status workflow
- Ticket queues and priority sorting
- Reports and ticket search
- Engineering Understanding Check quiz
- Integration and testing of project features

## Features

### 1. Ticket Management

- Create support tickets.
- Validate ticket information.
- Calculate ticket priority.
- Assign tickets to staff members.
- Update ticket statuses.
- Find existing tickets by ID.

### 2. Ticket Validation and Workflow Safety

- Reject invalid ticket information.
- Validate ticket categories, urgency, and affected-user counts.
- Reject blank staff assignments.
- Prevent unassigned tickets from moving to `in_progress`.
- Enforce valid ticket status transitions.
- Prevent invalid operations on resolved tickets.

### 3. Ticket Queues

- Retrieve open tickets.
- Retrieve tickets assigned to a staff member.
- Sort tickets by priority.
- Filter assigned and unassigned tickets.

### 4. Ticket Search

- Search tickets using supported filters.
- Filter search results.
- Sort search results by priority.

### 5. Follow-up Notes

- Add notes to tickets.
- View existing ticket notes.
- Validate note content and author information.
- Preserve notes when ticket data is saved and loaded.

### 6. Reports

Available reports include:
- Total ticket count.
- Ticket counts by status.
- Ticket counts by priority.
- Ticket counts by category.
- Assigned and unassigned ticket counts.
- Resolution statistics.

### 7. Data Storage

- Store ticket data in JSON format.
- Load previously saved tickets.
- Preserve ticket information between application runs.
- Validate loaded data.
- Handle missing or corrupted storage files.
- Detect invalid or duplicate ticket identifiers.

### 8. Engineering Understanding Check

The application includes a quiz to assess understanding of the system's design and implementation. It evaluates users' knowledge and calculates a score based on their answers.

## Ticket Priority Rules

Ticket priority is determined by urgency and the number of affected users.

The rules are evaluated in this order:

1. High urgency and at least 10 affected users: `critical`
2. High urgency or at least 10 affected users: `high`
3. Medium urgency or at least 3 affected users: `medium`
4. Otherwise: `low`

The `critical` rule must be checked before the `high` rule to ensure tickets meeting the critical condition receive the correct priority.

## Technologies Used

- Python 3
- Python standard library
- JSON for data storage
- `unittest` for automated testing
- Git and GitHub for version control and collaboration

No third-party Python packages are required for the core application.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aemmyo/campusflow-next-team-A-B.git
```
## Enter the Project Directory

``` bash
cd campusflow-next-team-A-B
```

## Running the Application

From the project root, run:

```bash
python3 main.py
```
Follow the prompts displayed in the terminal.

The menu provides options for managing tickets, assignments, queues, reports, search, notes, the Engineering Understanding Check, and saving before exiting.

## Running the Tests

CampusFlow Next uses Python's built-in unittest framework.

Run all tests from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The test suite covers:
- Ticket creation and validation
- Ticket storage and data handling
- Ticket assignment and status workflows
- Ticket queues and priority sorting
- Ticket notes
- Search functionality
- Reports
- Engineering Understanding Check scoring
- Command-line input and invalid choices

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
│   ├── baseline-check.md
│   ├── design-decisions.md
│   ├── ai-learning-log.md
│   └── ai-learning-log-engineer-b.md
└── README.md

## Project Documentation

Additional documentation is available in the docs/ directory.
- baseline-check.md — Baseline reliability assessment and findings.
- design-decisions.md — Important design decisions and implementation rationale.
- ai-learning-log.md — Shared AI learning log.
- ai-learning-log-engineer-b.md — Engineer B's learning log and reflections.

## Project Goals
CampusFlow Next aims to provide a simple, reliable, and maintainable helpdesk ticketing system while demonstrating:
- Good programming practices
- Input validation and error handling
- Modular software design
- Reliable data storage
- Automated testing
- Team collaboration
- Responsible use of AI as a learning and development aid
