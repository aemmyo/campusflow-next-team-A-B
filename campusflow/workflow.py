from campusflow.tickets import find_ticket
from campusflow.validation import (
    ALLOWED_TRANSITIONS,
    validate_assignment,
    validate_status,
)


def assign_ticket(tickets, ticket_id, staff):
    validate_assignment(staff)
    staff = staff.strip()

    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError(
            "Reopen the ticket before changing its assignment."
        )

    ticket["assigned_to"] = staff

    return ticket


def update_ticket_status(tickets, ticket_id, new_status):
    new_status = validate_status(new_status)

    ticket = find_ticket(tickets, ticket_id)
    current_status = ticket["status"]

    allowed_statuses = ALLOWED_TRANSITIONS.get(
        current_status,
        set(),
    )

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Cannot change status from {current_status} "
            f"to {new_status}."
        )

    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError(
            "Assign the ticket before starting work."
        )

    ticket["status"] = new_status

    return ticket