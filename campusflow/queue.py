"""Functions for viewing and sorting helpdesk tickets."""

from campusflow.tickets import PRIORITY_ORDER


def get_open_tickets(tickets):
    """Return tickets that are currently open."""
    return [
        ticket
        for ticket in tickets
        if ticket.get("status") == "open"
    ]


def get_assigned_tickets(tickets, staff_name):
    """Return tickets assigned to a particular staff member."""

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must not be blank")

    staff_name = staff_name.strip().casefold()

    return [
        ticket
        for ticket in tickets
        if isinstance(ticket.get("assigned_to"), str)
        and ticket["assigned_to"].strip().casefold() == staff_name
    ]


def sort_tickets_by_priority(tickets):
    """Return tickets sorted from highest to lowest priority."""

    return sorted(
        tickets,
        key=lambda ticket: PRIORITY_ORDER.get(
            ticket.get("priority"),
            len(PRIORITY_ORDER),
        ),
    )