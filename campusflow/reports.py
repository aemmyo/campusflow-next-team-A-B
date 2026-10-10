"""Reporting functions for CampusFlow tickets."""


def get_ticket_summary(tickets):
    """Return the total number of tickets."""
    return {
        "total": len(tickets),
    }


def count_tickets_by_status(tickets):
    """Count tickets grouped by status."""
    counts = {}

    for ticket in tickets:
        status = ticket.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1

    return counts


def count_tickets_by_priority(tickets):
    """Count tickets grouped by priority."""
    counts = {}

    for ticket in tickets:
        priority = ticket.get("priority", "unknown")
        counts[priority] = counts.get(priority, 0) + 1

    return counts


def count_tickets_by_category(tickets):
    """Count tickets grouped by category."""
    counts = {}

    for ticket in tickets:
        category = ticket.get("category", "unknown")
        counts[category] = counts.get(category, 0) + 1

    return counts


def count_assignment_status(tickets):
    """Count assigned and unassigned tickets."""
    assigned = sum(
        1
        for ticket in tickets
        if isinstance(ticket.get("assigned_to"), str)
        and ticket["assigned_to"].strip()
    )

    return {
        "assigned": assigned,
        "unassigned": len(tickets) - assigned,
    }