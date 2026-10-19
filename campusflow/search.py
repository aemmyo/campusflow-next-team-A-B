"""Ticket search, filtering, and sorting for CampusFlow."""

from campusflow.validation import (
    ALLOWED_CATEGORIES,
    ALLOWED_PRIORITIES,
    ALLOWED_STATUSES,
)
from campusflow.tickets import PRIORITY_ORDER

def search_tickets(
    tickets,
    title="",
    category="",
    status="",
    priority="",
):
    """Search tickets using optional filters.

    All supplied filters must match.
    Empty filters are ignored.
    The original ticket list is not modified.
    """

    # Validate the types of the search inputs.
    filters = {
        "title": title,
        "category": category,
        "status": status,
        "priority": priority,
    }

    for name, value in filters.items():
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string.")

    # Normalize the search inputs.
    title = title.strip().casefold()
    category = category.strip().lower()
    status = status.strip().lower()
    priority = priority.strip().lower()

    # Validate category.
    if category and category not in {
        item.casefold() for item in ALLOWED_CATEGORIES
    }:
        allowed_categories = ", ".join(sorted(ALLOWED_CATEGORIES))
        raise ValueError(
            f"Invalid category '{category}'. "
            f"Allowed categories: {allowed_categories}"
        )

    # Validate status.
    if status and status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Allowed statuses: {', '.join(ALLOWED_STATUSES)}"
        )

    # Validate priority.
    if priority and priority not in ALLOWED_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{priority}'. "
            f"Allowed priorities: {', '.join(sorted(ALLOWED_PRIORITIES))}"
        )

    results = []

    for ticket in tickets:

        # Match part of the title, ignoring letter case.
        if title and title not in ticket["title"].casefold():
            continue

        # Match category.
        if category and ticket["category"].lower() != category:
            continue

        # Match status.
        if status and ticket["status"].lower() != status:
            continue

        # Match priority.
        if priority and ticket["priority"].lower() != priority:
            continue

        # Include the ticket only if every supplied filter matches.
        results.append(ticket)

    return results


def sort_search_results_by_priority(tickets):
    """Sort search results by priority, then numeric ticket ID."""

    def sort_key(ticket):
        ticket_id = ticket["id"]

        # Convert T001 to 1, T002 to 2, and so on.
        numeric_id = int(ticket_id[1:])

        return (
            PRIORITY_ORDER.get(ticket["priority"], len(PRIORITY_ORDER)),
            numeric_id,
        )

    return sorted(tickets, key=sort_key)
