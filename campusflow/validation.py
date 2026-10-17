ALLOWED_CATEGORIES = {
    "Network",
    "Hardware",
    "Software",
    "Other",
}

ALLOWED_URGENCIES = {
    "low",
    "medium",
    "high",
}

ALLOWED_STATUSES = {
    "open",
    "in_progress",
    "resolved",
}

ALLOWED_PRIORITIES = {
    "low",
    "medium",
    "high",
    "critical",
}

REQUIRED_TICKET_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
    "notes",
}

# Keep the allowed status transitions in one place.
ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"open", "resolved"},
    "resolved": {"open"},
}


def validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")


def validate_category(category):
    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    allowed_categories = {
        item.casefold() for item in ALLOWED_CATEGORIES
    }

    if category.strip().casefold() not in allowed_categories:
        raise ValueError("Invalid ticket category.")


def normalize_category(category):
    validate_category(category)

    for item in ALLOWED_CATEGORIES:
        if item.casefold() == category.strip().casefold():
            return item


def validate_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")

    if urgency.strip().lower() not in ALLOWED_URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")


def validate_affected_users(affected_users):
    # bool is a subclass of int in Python.
    # type(...) is int rejects True and False.
    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError(
            "Affected users must be a positive integer."
        )


def validate_assignment(staff):
    if not isinstance(staff, str) or not staff.strip():
        raise ValueError("Staff name cannot be empty.")


def validate_status(status):
    if not isinstance(status, str):
        raise ValueError("Status must be a string.")

    status = status.strip().lower()

    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid ticket status: {status}")

    return status


def validate_note_author(author):
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Author cannot be empty.")

    return author.strip()


def validate_note_message(message):
    if not isinstance(message, str):
        raise ValueError("Message must be text.")

    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError(
            "Message must contain 5 to 300 characters."
        )

    return message


def calculate_priority(urgency, affected_users):
    validate_urgency(urgency)
    validate_affected_users(affected_users)

    urgency = urgency.strip().lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def validate_ticket_id(ticket_id):
    if (
        not isinstance(ticket_id, str)
        or len(ticket_id) < 2
        or not ticket_id.startswith("T")
        or not ticket_id[1:].isdigit()
        or int(ticket_id[1:]) < 1
    ):
        raise ValueError("Invalid ticket ID.")


def validate_note_id(note_id):
    if (
        not isinstance(note_id, str)
        or len(note_id) < 2
        or not note_id.startswith("N")
        or not note_id[1:].isdigit()
        or int(note_id[1:]) < 1
    ):
        raise ValueError("Invalid note ID.")


def validate_ticket(ticket):
    if not isinstance(ticket, dict):
        raise ValueError("Each ticket must be a dictionary.")

    missing = REQUIRED_TICKET_FIELDS - ticket.keys()

    if missing:
        raise ValueError(
            f"Ticket is missing required fields: {sorted(missing)}"
        )

    validate_ticket_id(ticket["id"])
    validate_title(ticket["title"])
    validate_category(ticket["category"])
    validate_urgency(ticket["urgency"])
    validate_affected_users(ticket["affected_users"])

    if ticket["category"] != normalize_category(ticket["category"]):
        raise ValueError("Ticket category is not normalized.")

    if ticket["urgency"] not in ALLOWED_URGENCIES:
        raise ValueError("Ticket urgency is not normalized.")

    if ticket["status"] not in ALLOWED_STATUSES:
        raise ValueError("Invalid ticket status.")

    expected_priority = calculate_priority(
        ticket["urgency"],
        ticket["affected_users"],
    )

    if ticket["priority"] != expected_priority:
        raise ValueError(
            "Ticket priority does not match its inputs."
        )

    assigned_to = ticket["assigned_to"]

    if assigned_to is not None:
        validate_assignment(assigned_to)

    if not isinstance(ticket["notes"], list):
        raise ValueError("Ticket notes must be a list.")

    seen_note_ids = set()

    for note in ticket["notes"]:
        if not isinstance(note, dict):
            raise ValueError("Each note must be a dictionary.")

        if set(note.keys()) != {"note_id", "author", "message"}:
            raise ValueError("Note has an invalid structure.")

        validate_note_id(note["note_id"])

        if note["note_id"] in seen_note_ids:
            raise ValueError("Duplicate note ID.")

        seen_note_ids.add(note["note_id"])

        validate_note_author(note["author"])
        validate_note_message(note["message"])


def validate_ticket_collection(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Ticket collection must be a list.")

    seen_ids = set()

    for ticket in tickets:
        validate_ticket(ticket)

        if ticket["id"] in seen_ids:
            raise ValueError("Duplicate ticket ID.")

        seen_ids.add(ticket["id"])