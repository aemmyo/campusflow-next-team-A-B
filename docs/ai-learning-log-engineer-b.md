# AI Learning Log - Engineer B

## Interaction 1: Ticket Status Workflow

**Tool:** ChatGPT

**Problem:** I needed to understand how ticket assignment and
status updates should work without allowing invalid transitions.

**Initial understanding:** I understood that tickets have statuses,
but I needed to understand how to enforce the allowed transitions
and prevent rejected actions from changing ticket data.

**AI guidance:** I used AI to discuss status-transition rules,
assignment requirements, and ways to test valid and invalid changes.

**My verification:** I examined the workflow implementation and
ran the workflow unit tests. The tests checked valid transitions,
invalid transitions, and attempts to start work on an unassigned
ticket.

**Learning:** I learned that workflow rules should be enforced
in the application logic rather than relying only on CLI input.

## Interaction 2: Investigating the Baseline Startup Failure

**Tool:** ChatGPT and terminal experiments

**Problem:** The original application failed before displaying
the menu.

**Initial understanding:** I needed to identify whether the error
came from the CLI or the storage implementation.

**Investigation:** I ran the baseline application and inspected
the traceback. I then compared the call to `load_tickets()` in
the CLI with the function definition in the storage module.

**Finding:** The CLI called `load_tickets()` without an argument,
while the function required a file path. I also found that the
baseline save call omitted the required path argument.

**Verification:** I reproduced the startup error. The save-call
problem was confirmed by source inspection, not a runtime test.

**Learning:** I learned that a function call must match the
function's parameter requirements. I also learned to distinguish
a reproduced runtime failure from a problem identified only
through source inspection.

## Interaction 3: Understanding print() and return

**Tool:** ChatGPT and small Python experiments

**Problem:** I needed to understand the difference between
displaying a message and returning a value from a function.

**Initial understanding:** I knew that `print()` displays text,
but I needed to understand how a function passes a result back
to the code that called it.

**Experiment:** I compared a function that prints a value with
a function that returns a value, then examined how the caller
could use each result.

**Verification:** I observed the experiment's output and checked
whether the caller could store and use the returned value.

**Learning:** I learned that `print()` displays information,
while `return` sends a result back to the caller. A function
can return a value without printing it.

## Interaction 4: Debugging Search Filter Input

**Tool:** ChatGPT and terminal tests

**Problem:** I investigated why category filter input such as
`network` could be rejected even when `network` was an allowed
category.

**Initial understanding:** I needed to check whether the problem
was caused by the accepted category values or by how user input
was compared with them.

**Investigation:** I examined the filter-validation logic and
compared the normalized user input with the allowed values.

**Change:** I updated the comparison to use normalized allowed
values as well as normalized user input.

**Verification:** I manually tested lowercase category input
and ran the automated test suite. The latest recorded test run
passed all 111 tests.

**Learning:** I learned that normalizing only the user's input
is insufficient if the values being compared use a different
letter case.

## Final Verification

**Command:**

`python3 -m unittest discover -s tests -v`

**Recorded result:** 111 tests passed.

**Reflection:** AI helped me investigate errors and understand
design choices, but its suggestions still needed to be checked.
I used source inspection, terminal experiments, and automated
tests to verify behaviour. I learned to investigate the cause
of a problem rather than relying only on a suggested fix.
