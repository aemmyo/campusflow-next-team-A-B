import json
import os
import tempfile
from pathlib import Path

from campusflow.validation import validate_ticket_collection


def save_tickets(tickets, path):
    """
    Validate and save tickets to a JSON file.

    Existing JSON files using either a list or a
    {"tickets": [...]} envelope retain their format.
    New files use a list.
    """

    validate_ticket_collection(tickets)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Preserve the existing file's format where possible.
    envelope = False

    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as file:
                existing_data = json.load(file)

            envelope = (
                isinstance(existing_data, dict)
                and set(existing_data.keys()) == {"tickets"}
                and isinstance(existing_data["tickets"], list)
            )

        except (OSError, json.JSONDecodeError):
            # A malformed old file must not prevent saving
            # the currently validated collection.
            envelope = False

    data = {"tickets": tickets} if envelope else tickets

    # Write a temporary file first, then replace the target.
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
        ) as file:
            temporary_path = Path(file.name)

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, path)

    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def load_tickets(path):
    """
    Load and validate the entire collection.

    Returns a new list. Does not modify an existing
    in-memory ticket collection.
    """

    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            "The ticket file contains invalid JSON."
        ) from error

    if isinstance(data, dict):
        if set(data.keys()) != {"tickets"}:
            raise ValueError("Invalid JSON envelope.")

        data = data["tickets"]

    # Validate everything before returning any records.
    try:
        validate_ticket_collection(data)

    except (ValueError, TypeError, KeyError) as error:
        raise ValueError(
            f"Ticket file failed validation: {error}"
        ) from error

    # Give the application its own collection of dictionaries.
    return json.loads(json.dumps(data))