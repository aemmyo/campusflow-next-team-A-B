import json
import os
import tempfile
from pathlib import Path

from campusflow.validation import validate_ticket_collection


def _read_ticket_file(path):
    """
    Read and validate an existing ticket file.

    Supports both:
        [...]
    and:
        {"tickets": [...]}

    Returns:
        A tuple containing the ticket list and whether the
        original file uses the envelope format.

    Raises:
        OSError: If the file cannot be read.
        ValueError: If the JSON or ticket collection is invalid.
    """
    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"The ticket file contains invalid JSON: {path}"
        ) from error

    envelope = False

    if isinstance(data, dict):
        if set(data.keys()) != {"tickets"}:
            raise ValueError(
                f"Invalid JSON envelope in {path}."
            )

        if not isinstance(data["tickets"], list):
            raise ValueError(
                f"The tickets field must contain a list: {path}"
            )

        data = data["tickets"]
        envelope = True

    try:
        validate_ticket_collection(data)

    except (ValueError, TypeError, KeyError) as error:
        raise ValueError(
            f"Ticket file failed validation: {error}"
        ) from error

    return data, envelope


def save_tickets(tickets, path):
    """
    Validate and safely save tickets to a JSON file.

    Features:
        - Validates tickets before saving.
        - Creates missing parent directories.
        - Preserves the existing JSON envelope format.
        - Writes to a temporary file before replacing the target.
        - Refuses to overwrite an existing file that cannot be
          read, parsed, or validated.
        - Removes temporary files after failed writes.

    New files use a JSON list.
    """
    path = Path(path)

    # Validate the collection before performing file operations.
    validate_ticket_collection(tickets)

    # Preserve the existing format when the target already exists.
    envelope = False

    if path.exists():
        _, envelope = _read_ticket_file(path)

    # Create the parent directory if it does not exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Prepare the data in the appropriate JSON format.
    data = {"tickets": tickets} if envelope else tickets

    temporary_path = None

    try:
        # Create the temporary file in the target directory so that
        # os.replace() can replace the target on the same filesystem.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

            # Flush Python's buffered output to the operating system.
            file.flush()

            # Request that the operating system flush file contents.
            os.fsync(file.fileno())

        # Replace the target only after the temporary file is written.
        os.replace(temporary_path, path)

        # The temporary path no longer exists after a successful replace.
        temporary_path = None

    finally:
        # Clean up a temporary file if writing or replacement failed.
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                # Do not replace the original saving error with a
                # cleanup error. The leftover file can be inspected.
                pass


def load_tickets(path):
    """
    Load and validate the entire ticket collection.

    Supports both a JSON list and a {"tickets": [...]} envelope.

    Returns:
        A new list containing the loaded tickets.

    Raises:
        OSError: If the file cannot be opened or read.
        ValueError: If the JSON or ticket collection is invalid.
    """
    path = Path(path)

    tickets, _ = _read_ticket_file(path)

    # Return an independent copy so callers do not receive the
    # same mutable collection object created by the JSON parser.
    return json.loads(json.dumps(tickets))