# AI Learning Log - Engineer B

## Interaction 1: Ticket Status Workflow

Tool: ChatGPT

Task: Implement ticket assignment and status updates.

Learning: I learned that a ticket workflow must enforce valid status transitions and reject invalid changes.

Verification: Tested valid and invalid status transitions using unit tests.

## Interaction 2: Ticket Queue

Tool: ChatGPT

Task: Organize tickets by priority and retrieve tickets assigned to staff.

Learning: I learned how sorting, filtering, and case-insensitive staff-name matching help organize tickets.

Verification: Tested priority sorting, staff assignment, and filtering.

## Interaction 3: Search, Notes, and Reports

Tool: ChatGPT

Task: Implement ticket search, notes, and reporting features.

Learning: I learned the importance of testing search filters, handling empty data, and validating operations.

Verification: Ran the relevant unit tests.

## Interaction 4: Engineering Understanding Quiz

Tool: ChatGPT

Task: Develop a quiz to assess understanding of CampusFlow.

Learning: I learned that automated tests can verify behavior, but I must also understand the implementation and explain design decisions.

Verification: Tested quiz scoring and command-line behavior.

## Final Verification

Command: python3 -m unittest discover -s tests -v

Result: 106 tests passed.

Reflection: AI assisted me during development, but I need to review the code, understand the logic, test edge cases, and ensure that the implementation meets the project requirements.
