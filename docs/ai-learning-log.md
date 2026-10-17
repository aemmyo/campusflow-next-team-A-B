# AI Learning Log - Engineer A (Felix)

## Interaction 1: Initial Scaffolding
Tool: ChatGPT / Claude
Prompt: Give me ticket creation function
AI Output: Suggested basic function with title, category but no validation
My Action: Accepted structure, but added my own validation (blank title, zero users, decimal check) because AI missed edge cases.
Learning: AI gives happy path, I must add edge cases.

## Interaction 2: Priority Engine - THE CRITICAL REJECTION
Tool: Claude.ai (Screenshot Oct 9 15:56)
Prompt: Write calculate_priority(urgency, affected_users) with rules
AI Output: AI suggested OR before AND - if high or >=10 return high, then if high and >=10 return critical (UNREACHABLE)
My Test: Tested calculate_priority(high, 12) returned high but expected critical
Why Wrong: OR condition catches high+12 first, AND never runs. Rule order matters.
My Fix: REJECTED AI order. I reordered to check AND first:
  if urgency == high and affected_users >= 10: return critical
  if urgency == high or affected_users >= 10: return high
Test After Fix: high+12 = critical OK, high+2 = high OK, medium+10 = high OK
Test File: tests/test_tickets.py TestPriorityEngine test_rule_order_critical_over_high
Learning: AI doesn't understand rule precedence. Critical must be checked before High.

## Interaction 3: ID Generation
Tool: ChatGPT
AI Output: Suggested next_id = T + len(tickets)+1
My Action: Rejected. After save/load/delete, len gives duplicate IDs.
My Fix: Parse max ID: max(int(t[id][1:]) for t in tickets) + 1
Test: test_id_unique_after_reload in test_storage.py

## Interaction 4: Storage Error Handling
Tool: Copilot
AI Output: Suggested except return [] on JSON load
My Action: Rejected. Returning [] on corrupted JSON silently deletes all tickets.
My Fix: Raise ValueError Malformed JSON so CLI can show error
Test: test_malformed_json_raises

Summary
Total AI interactions: 4
Accepted: 0 as-is, 4 with major modifications
Rejected: 2 critical logic errors (priority order, ID generation)
Final verification: 19 tests OK
---

# AI Learning Log - Engineer B

## Interaction 1: Ticket Status Workflow

Tool: ChatGPT

Task: Implement ticket assignment and status updates.

Learning: I learned that a ticket workflow must enforce valid status transitions and reject invalid changes.

Verification: The workflow tests cover valid transitions, invalid transitions, and attempts to start work on an unassigned ticket.

## Interaction 2: Ticket Queue

Tool: ChatGPT

Task: Organize tickets by priority and retrieve tickets assigned to staff.

Learning: I learned how sorting, filtering, and case-insensitive staff-name matching help organize tickets.

Verification: The queue tests cover priority sorting, assigned-ticket retrieval, case-insensitive matching, and preserving the original list.

## Interaction 3: Search, Notes, and Reports

Tool: ChatGPT

Task: Implement ticket search, notes, and reporting features.

Learning: I learned the importance of combining search filters, validating input, handling empty results, and preserving notes through ticket status changes.

Verification: The search, notes, and reports tests passed in the full test suite.

## Interaction 4: Engineering Understanding Quiz

Tool: ChatGPT

Task: Develop a quiz to assess understanding of CampusFlow.

Learning: I learned that automated tests can verify behavior, but I must also understand the implementation and explain design decisions.

Verification: The quiz tests passed in the full test suite.

## Critical Evaluation: AI Suggestions and Verification

### Situation
While developing CampusFlow, I used AI to help understand
ticket workflows, search filters, and error handling.

### Critical Evaluation
I learned that an AI-generated explanation or code change
should not automatically be treated as correct. For example,
when investigating the baseline startup failure, I compared
the original CLI call with the storage function definition
and checked the reported error. This allowed me to verify
the missing path argument instead of relying only on an
AI explanation.

I also verified implementation behaviour through unit tests
and terminal experiments. Passing tests provide useful
evidence, but they do not prove that every requirement or
edge case has been covered.

### Final Decision
I treated AI as a development aid rather than the final
authority. I used source inspection, experiments, and tests
to evaluate its suggestions before accepting a conclusion.

### Learning
I learned to question proposed solutions, verify claims
independently, and distinguish tested behaviour from
assumptions or untested possibilities.

## Learning Cycle 1: Python List Comprehensions

### Original Knowledge Gap
I wanted to understand how Python can transform every item in a list without writing a traditional loop.

### Question / Learning Goal
I asked ChatGPT to help me practise using a Python list comprehension to calculate the square of each number in a list.

### AI Guidance
ChatGPT suggested using the expression `[n * n for n in numbers]`. This takes each number from the list, multiplies it by itself, and collects the results in a new list.

### Independent Experiment
I ran this command in my terminal:

`python3 -c 'numbers = [1, 2, 3, 4]; squares = [n * n for n in numbers]; print(squares)'`

### Verification
Actual output:

`[1, 4, 9, 16]`

The output matched the expected result. I verified it by running the command myself.

### Final Decision
I accepted the explanation after checking the output.

### Reflection
I learned that a small experiment can help me understand code and verify an explanation instead of relying on AI alone.

---

## Learning Cycle 2: Investigating the CampusFlow Baseline Failure

### Original Knowledge Gap
I needed to understand why the original CampusFlow CLI failed before displaying its menu.

### Question
I asked ChatGPT to help me investigate the baseline failure and verify whether the storage function required a path argument.

### AI Guidance
ChatGPT guided me to compare the storage function definition with the original CLI call.

### Independent Verification
I inspected the original baseline source using:

`git show 0519c17:campusflow/storage.py`

`git show 0519c17:main.py`

I found the storage function definition:

`def load_tickets(path):`

I also found the original CLI call:

`tickets = load_tickets()`

The baseline application had previously produced:

`TypeError: load_tickets() missing 1 required positional argument: 'path'`

### Evidence-Based Decision
I recorded the mismatch in `docs/baseline-check.md`. The current CLI passes `DATA_FILE` to `load_tickets()`, and the two CLI tests passed, including the save-and-exit test.

### Reflection
I learned to compare a function's definition with its call instead of guessing at the cause of an error. I also learned to distinguish confirmed findings from behaviour that has not been tested.

## Independent Experiment 2: Python Functions and Return

### Learning Goal
I wanted to understand how a Python function calculates a value and returns it to the caller.

### AI Guidance
ChatGPT explained the difference between defining a function, calling it, and printing its returned value.

### Experiment
I ran the following command:

`python3 -c 'def calculate_total(price, quantity): return price * quantity
print(calculate_total(500, 3))'`

### Verification
Actual output: `1500`

The output matched the expected result.

### Reflection
I learned that `return` sends a result back to the caller, while `print()` displays a value on the screen.

## Engineer B Summary

These learning cycles helped me practise independent experimentation, source-code inspection, and evidence-based debugging. I learned that AI can guide an investigation, but I must verify its suggestions through experiments, code inspection, and test results.

## Final Verification

Command: `python3 -m unittest discover -s tests -v`

Result: 106 tests passed.

Output: `Ran 106 tests in 0.107s — OK`

Reflection: Running the complete test suite helped me verify that the existing ticket workflow, queue, search, notes, reports, quiz, validation, storage, and CLI tests all passed together.
