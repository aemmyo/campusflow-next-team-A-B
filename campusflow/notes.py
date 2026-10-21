from campusflow.tickets import find_ticket

from campusflow.validation import (
    validate_note_id,
    validate_note_author,
    validate_note_message,
)


def next_note_id(ticket):
    highest_id = 0

    for note in ticket["notes"]:
        validate_note_id(note["note_id"])

        number = int(note["note_id"][1:])
        highest_id = max(highest_id, number)

    return f"N{highest_id + 1:03d}"


def add_note(tickets, ticket_id, author, message):
    # Find the ticket before making any changes.
    ticket = find_ticket(tickets, ticket_id)

    # Notes cannot be added to resolved tickets.
    if ticket["status"] not in {"open", "in_progress"}:
        raise ValueError(
            "Cannot add notes to a resolved ticket."
        )

    # Use the shared validation functions.
    author = validate_note_author(author)
    message = validate_note_message(message)

    # Generate the ID only after validating the input.
    note = {
        "note_id": next_note_id(ticket),
        "author": author,
        "message": message,
    }

    ticket["notes"].append(note)

    return note


def get_notes(tickets, ticket_id):
    ticket = find_ticket(tickets, ticket_id)

    # Return a new list so callers cannot rearrange the
    # ticket's stored notes by sorting this result.
    return sorted(
        ticket["notes"],
        key=lambda note: int(note["note_id"][1:]),
    )