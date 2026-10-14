from campusflow.validation import (
    validate_title,
    validate_category,
    normalize_category,
    validate_urgency,
    validate_affected_users,
    validate_assignment,
    validate_ticket_id,
    calculate_priority,
)

PRIORITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


def find_ticket(tickets, ticket_id):
    validate_ticket_id(ticket_id)

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} was not found.")


def next_ticket_id(tickets):
    highest_id = 0

    for ticket in tickets:
        validate_ticket_id(ticket["id"])
        number = int(ticket["id"][1:])
        highest_id = max(highest_id, number)

    return f"T{highest_id + 1:03d}"


def create_ticket(
    tickets,
    title,
    category,
    urgency,
    affected_users,
):
    # Validate everything before changing the collection.
    validate_title(title)
    validate_category(category)
    validate_urgency(urgency)
    validate_affected_users(affected_users)

    ticket_id = next_ticket_id(tickets)

    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": normalize_category(category),
        "urgency": urgency.strip().lower(),
        "affected_users": affected_users,
        "priority": calculate_priority(
            urgency,
            affected_users,
        ),
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }

    tickets.append(ticket)

    return ticket


def assign_ticket(tickets, ticket_id, staff):
    # Validate the requested change before modifying the ticket.
    validate_assignment(staff)

    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError(
            "Reopen the ticket before changing its assignment."
        )

    ticket["assigned_to"] = staff.strip()

    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)

    allowed_transitions = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
        "resolved": {"open"},
    }

    if new_status not in allowed_transitions:
        raise ValueError("Invalid ticket status.")

    current_status = ticket["status"]

    if new_status not in allowed_transitions[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} "
            f"to {new_status}."
        )

    if (
        new_status == "in_progress"
        and not ticket["assigned_to"]
    ):
        raise ValueError(
            "Assign the ticket before starting work."
        )

    ticket["status"] = new_status

    return ticket