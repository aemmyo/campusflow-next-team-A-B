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