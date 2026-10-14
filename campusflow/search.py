"""Ticket search, filtering, and sorting for CampusFlow."""

from campusflow.tickets import ALLOWED_CATEGORIES, PRIORITY_ORDER


ALLOWED_STATUSES = ["open", "in_progress", "resolved"]


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

    # Normalize the search inputs.
    title = title.strip().casefold() if title else ""
    category = category.strip().lower() if category else ""
    status = status.strip().lower() if status else ""
    priority = priority.strip().lower() if priority else ""

    # Validate category.
    if category and category not in ALLOWED_CATEGORIES:
        raise ValueError(
            f"Invalid category '{category}'. "
            f"Allowed categories: {', '.join(ALLOWED_CATEGORIES)}"
        )

    # Validate status.
    if status and status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Allowed statuses: {', '.join(ALLOWED_STATUSES)}"
        )

    # Validate priority.
    if priority and priority not in PRIORITY_ORDER:
        raise ValueError(
            f"Invalid priority '{priority}'. "
            f"Allowed priorities: {', '.join(PRIORITY_ORDER)}"
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