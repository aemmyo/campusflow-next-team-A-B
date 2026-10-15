# CampusFlow AI Learning Log

## Purpose

This document records how AI assistance was used during
CampusFlow development.

The purpose is to demonstrate learning, critical thinking,
verification, and responsible use of AI-generated suggestions.

## Interaction 1: Ticket Assignment Safety

### Engineer
Engineer A — Ticket Safety and Storage

### Topic
Preventing unsafe ticket reassignment.

### Question or Prompt
[Record the actual question asked of the AI.]

### AI Suggestion
[Summarize the actual suggestion received.]

### Verification
The implementation was checked against the ticket assignment
requirements and the automated tests.

Relevant test:
`test_resolved_ticket_cannot_be_reassigned`

### Outcome
[Explain what was accepted, changed, or rejected and why.]

### Learning
Ticket assignment must respect the current state of a ticket.
A resolved ticket must be reopened before its assignment can
be changed.

---

## Interaction 2: Ticket Status Transitions

### Engineer
Engineer A — Ticket Safety and Storage

### Topic
Enforcing valid ticket status transitions.

### Question or Prompt
[Record the actual question asked of the AI.]

### AI Suggestion
[Summarize the actual suggestion received.]

### Verification
The implementation was checked using the workflow test suite.

Relevant tests include:

- `test_invalid_transition_is_rejected`
- `test_unassigned_ticket_cannot_start_work`
- `test_resolved_ticket_cannot_restart_directly`

### Outcome
[Describe the actual changes made after reviewing the suggestion.]

### Learning
Workflow rules should be enforced consistently, and invalid
operations should produce appropriate errors.

---

## Interaction 3: Debugging and Test Verification

### Engineer
Engineer A — Ticket Safety and Storage

### Topic
Using automated tests to identify and correct a workflow bug.

### Question or Prompt
[Record the actual debugging question asked of the AI.]

### Problem Observed
The test `test_resolved_ticket_cannot_be_reassigned`
failed because the expected ValueError was not raised.

### AI Suggestion
The workflow assignment function needed to reject assignment
changes when a ticket was resolved.

### Verification
The workflow implementation was updated and the automated
test suite was run again.

Latest verified result:

`Ran 85 tests ... OK`

### Outcome
The latest test run passed all 85 tests.

### Learning
A test failure provides evidence about application behavior.
The implementation should be corrected and tested again rather
than assuming that the original code is correct.

---

## Interaction 4: Engineer B

### Engineer
Engineer B — Search, Reports, and CLI

### Topic
[Record the actual topic.]

### Question or Prompt
[Record the actual question asked of the AI.]

### AI Suggestion
[Summarize the actual suggestion received.]

### Verification
[Explain how Engineer B checked the suggestion, such as
running relevant tests or manually checking the output.]

### Outcome
[Explain what was accepted, modified, or rejected.]

### Learning
[Describe what Engineer B learned.]

---

## Critical Review of AI Suggestions

At least one AI suggestion must be evaluated critically.

### Original Suggestion
[Record the actual suggestion.]

### Evidence
[Identify the test result, requirement, or observed behavior
used to evaluate the suggestion.]

### Decision
[Explain whether the suggestion was accepted, improved,
or rejected.]

### Reason
[Explain why the evidence supported that decision.]

## Conclusion

AI assistance was used as a development and learning aid.
Suggestions were checked against application requirements,
implementation behavior, and automated tests.

The purpose of this log is to record actual interactions and
demonstrate that engineering decisions were verified rather
than accepted without review.