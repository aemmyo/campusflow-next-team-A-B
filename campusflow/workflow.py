from campusflow.tickets import find_ticket


# Defines the status changes allowed in CampusFlow.
ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"open", "resolved"},
    "resolved": {"open"},
}


def assign_ticket(tickets, ticket_id, staff_name):
    """
    Assign a ticket to a staff member.

    Rules:
    - The staff name must be a non-empty string.
    - The ticket must exist.
    - A resolved ticket cannot be reassigned.
    - Reopen a resolved ticket before changing its assignment.
    - Invalid operations must not modify the ticket.
    """

    # Validate the staff name before making any changes.
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")

    staff_name = staff_name.strip()

    # Find the requested ticket.
    ticket = find_ticket(tickets, ticket_id)

    # Prevent assignment changes on resolved tickets.
    if ticket["status"] == "resolved":
        raise ValueError(
            "Reopen the ticket before changing its assignment."
        )

    # Update the assignment only after validation succeeds.
    ticket["assigned_to"] = staff_name

    return ticket


def update_ticket_status(tickets, ticket_id, new_status):
    """
    Update a ticket's status.

    Allowed transitions:
    - open -> in_progress
    - in_progress -> open
    - in_progress -> resolved
    - resolved -> open

    An unassigned ticket cannot move to in_progress.
    Invalid operations must not modify the ticket.
    """

    # Validate the requested status.
    if not isinstance(new_status, str):
        raise ValueError("Status must be a string.")

    new_status = new_status.strip().lower()

    valid_statuses = {"open", "in_progress", "resolved"}

    if new_status not in valid_statuses:
        raise ValueError(f"Invalid ticket status: {new_status}")

    # Find the ticket.
    ticket = find_ticket(tickets, ticket_id)

    current_status = ticket["status"]

    # Check whether the requested transition is allowed.
    allowed_statuses = ALLOWED_TRANSITIONS.get(current_status, set())

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Cannot change ticket status from "
            f"'{current_status}' to '{new_status}'."
        )

    # A ticket must be assigned before work can begin.
    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError(
            "An unassigned ticket cannot be moved to in_progress."
        )

    # Update the status only after all validation succeeds.
    ticket["status"] = new_status

    return ticket