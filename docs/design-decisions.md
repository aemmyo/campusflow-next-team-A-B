# CampusFlow Design Decisions

This document records the main design decisions behind CampusFlow,
including ticket management, workflow, persistence, search, notes,
reporting, and the Engineering Understanding Check.

## 1. Priority Engine Order

**Decision:** Check the critical priority condition before the high
priority condition.

**Reason:** A ticket with high urgency and at least 10 affected users
must receive critical priority. Checking the broader high-priority
condition first would make the critical condition unreachable.

**Example:** High urgency with 12 affected users receives critical
priority.

**Verification:** The priority engine tests cover the priority rules
and their ordering.

## 2. Ticket ID Generation

**Decision:** Generate the next ticket ID from the highest existing
numeric ID rather than using the number of tickets plus one.

**Reason:** Counting tickets can produce duplicate IDs after tickets
are deleted or existing tickets are loaded from storage.

**Verification:** Ticket ID generation and storage tests check that
IDs remain unique after loading saved data.

## 3. Input Validation

**Decision:** Validate ticket information before accepting it.

Validation includes rejecting blank titles, invalid categories,
invalid urgency values, and affected-user counts that are zero,
negative, or not valid integers.

**Reason:** Early validation prevents invalid data from entering
the ticket collection.

**Verification:** The validation and ticket tests cover valid inputs
and common invalid values.

## 4. Storage: Missing Files and Corrupted Data

**Decision:** Treat a missing ticket file differently from corrupted
or invalid saved data.

A missing file represents a possible first application run and can
be handled by starting with an empty ticket collection. Corrupted JSON
or invalid stored records must produce an error rather than being
silently treated as an empty collection.

**Reason:** Silently replacing corrupted data with an empty collection
could hide a storage problem and risk losing existing ticket data.

**Implementation:** The command-line interface passes the configured
data-file path to the storage functions and handles relevant loading
errors.

**Verification:** Storage tests cover loading, saving, malformed JSON,
duplicate IDs, and invalid stored records.

## 5. Ticket Data Structure

**Decision:** Represent tickets as dictionaries containing fields
such as ID, title, category, urgency, affected users, priority,
status, and assignee.

**Reason:** Dictionaries provide a straightforward way to access ticket
properties and work with JSON persistence.

Tickets begin with an open status and no assigned staff member.

**Verification:** Ticket, workflow, and storage tests check ticket
creation, updates, and persistence.

## 6. Package Structure

**Decision:** Organize the application's functionality into modules
inside the `campusflow` package.

**Reason:** Separating responsibilities makes the code easier to
understand, maintain, and test.

The `__init__.py` file supports importing the package's modules.

## 7. Ticket Workflow and Assignment

**Decision:** Keep ticket assignment and status transitions in the
workflow functionality instead of placing all business logic in
the command-line interface.

**Reason:** Separating workflow rules from user interaction makes
the rules easier to test and reuse.

The workflow validates assignments and status changes. For example,
an unassigned ticket cannot be moved into the in-progress state.

**Verification:** Workflow tests cover valid transitions, invalid
transitions, assignment validation, and attempts to start work on
an unassigned ticket.

## 8. Ticket Queues

**Decision:** Provide separate functions for retrieving open tickets,
retrieving tickets assigned to staff, and sorting tickets by priority.

**Reason:** These operations help users identify outstanding work
and organize tickets for follow-up.

Queue operations should not unexpectedly modify the original ticket
collection when sorting results.

**Verification:** Queue tests cover retrieval, case-insensitive staff
matching, priority sorting, and preservation of the original list.

## 9. Ticket Search and Filtering

**Decision:** Keep search functionality in a dedicated search module.

Users can search ticket titles and filter results by category,
status, and priority. Search filters can be combined, and matching
is designed to be case-insensitive where applicable.

Search results can also be sorted by priority.

**Reason:** Separating search logic from the CLI allows the filtering
rules to be tested independently of user input and display code.

**Verification:** Search tests cover individual filters, combined
filters, case-insensitive title matching, invalid filters, empty
results, and sorting.

## 10. Ticket Notes

**Decision:** Store ticket notes through dedicated note-management
functions rather than mixing note operations with ticket creation
and workflow logic.

**Reason:** This keeps note validation and retrieval separate from
other ticket operations.

Notes include information such as a note ID, author, and message.
Validation rules help prevent blank authors and messages that fall
outside the accepted length limits.

**Verification:** Notes tests cover validation, note retrieval,
note IDs, and note behavior when ticket status changes.

## 11. Reports and Analytics

**Decision:** Use dedicated reporting functions to calculate ticket
summaries and counts by status, priority, category, and assignment.

**Reason:** Centralizing these calculations avoids duplicating
reporting logic throughout the CLI and makes the results easier
to test.

**Verification:** Report tests cover totals, category counts,
priority counts, status counts, and assignment statistics.

## 12. Engineering Understanding Check

**Decision:** Provide the Engineering Understanding Check as a
separate quiz module, with quiz questions maintained in a dedicated
question module.

**Reason:** Separating quiz execution from the question data makes
the quiz easier to maintain and test.

The quiz allows the user to answer questions and receive a score
after completing the assessment.

**Verification:** Quiz tests cover correct answers, incorrect
answers, empty answers, case-insensitive answer handling, and
displaying results after all six questions.

## 13. Command-Line Interface

**Decision:** Use `main.py` to connect the application's features
through a menu-driven command-line interface.

The menu provides access to ticket creation, listing, viewing,
assignment, status updates, priority queues, reports, search,
ticket notes, the Engineering Understanding Check, and saving
and exiting.

**Reason:** A menu-driven interface makes the application's
functionality accessible without requiring users to call Python
functions directly.

Input validation and error handling help the application respond
to invalid choices and relevant operational errors.

**Verification:** CLI tests cover invalid menu choices and saving
and exiting. Manual testing is also used to check user interactions.

## 14. Testing and Verification

**Decision:** Use Python's unittest framework to test individual
modules and the integrated application.

**Reason:** Automated tests help identify regressions when features
are changed or combined.

**Verification:** The recorded test run completed with 106 tests
passing. The suite covers ticket management, validation, workflow,
storage, queues, search, notes, reports, the quiz, and CLI behavior.

The test suite should be rerun after code changes so that the
documented result reflects the latest verification.

## 15. Lessons Learned

The project reinforced several engineering practices:

- Check specific conditions before broader conditions when rule
  ordering affects the result.
- Generate identifiers from existing data rather than assuming
  the number of records determines the next ID.
- Distinguish missing files from corrupted saved data.
- Separate business logic into modules that can be tested
  independently.
- Verify AI-generated suggestions through code inspection,
  experiments, and automated tests.
- Test feature integration as well as individual functions.
