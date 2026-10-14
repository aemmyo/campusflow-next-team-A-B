import json
import tempfile
import unittest

from pathlib import Path

from campusflow.tickets import create_ticket, next_ticket_id
from campusflow.notes import add_note, next_note_id
from campusflow.storage import save_tickets, load_tickets


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.addCleanup(self.temp_directory.cleanup)

        self.path = (
            Path(self.temp_directory.name) / "tickets.json"
        )

        self.tickets = []

        self.ticket = create_ticket(
            self.tickets,
            "Wi-Fi is not working",
            "Network",
            "high",
            10,
        )

    def test_save_tickets_creates_file(self):
        save_tickets(self.tickets, self.path)

        self.assertTrue(self.path.exists())

    def test_saved_file_contains_ticket(self):
        save_tickets(self.tickets, self.path)

        with self.path.open(encoding="utf-8") as file:
            saved_data = json.load(file)

        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0]["id"], "T001")

    def test_load_tickets(self):
        save_tickets(self.tickets, self.path)

        loaded_tickets = load_tickets(self.path)

        self.assertEqual(loaded_tickets, self.tickets)

    def test_notes_survive_save_and_load(self):
        add_note(
            self.tickets,
            "T001",
            "Mentor A",
            "Router reboot attempted",
        )

        save_tickets(self.tickets, self.path)

        loaded_tickets = load_tickets(self.path)

        self.assertEqual(
            loaded_tickets[0]["notes"][0]["note_id"],
            "N001",
        )

        self.assertEqual(
            loaded_tickets[0]["notes"][0]["message"],
            "Router reboot attempted",
        )

    def test_next_ticket_id_after_loading(self):
        create_ticket(
            self.tickets,
            "Laptop problem",
            "Hardware",
            "medium",
            3,
        )

        save_tickets(self.tickets, self.path)

        loaded_tickets = load_tickets(self.path)

        self.assertEqual(next_ticket_id(loaded_tickets), "T003")

    def test_next_note_id_after_loading(self):
        add_note(
            self.tickets,
            "T001",
            "Mentor A",
            "Router reboot attempted",
        )

        save_tickets(self.tickets, self.path)

        loaded_tickets = load_tickets(self.path)

        self.assertEqual(
            next_note_id(loaded_tickets[0]),
            "N002",
        )

    def test_corrupt_json_rejected(self):
        self.path.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_tickets(self.path)

    def test_duplicate_ticket_ids_rejected(self):
        duplicate = self.ticket.copy()
        duplicate["notes"] = []

        self.path.write_text(
            json.dumps([self.ticket, duplicate]),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_tickets(self.path)

    def test_duplicate_note_ids_rejected(self):
        self.ticket["notes"] = [
            {
                "note_id": "N001",
                "author": "Mentor A",
                "message": "Router reboot attempted",
            },
            {
                "note_id": "N001",
                "author": "Mentor B",
                "message": "Checking the network switch",
            },
        ]

        with self.assertRaises(ValueError):
            save_tickets(self.tickets, self.path)

    def test_invalid_status_rejected_during_load(self):
        invalid_ticket = self.ticket.copy()
        invalid_ticket["status"] = "cancelled"

        self.path.write_text(
            json.dumps([invalid_ticket]),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_tickets(self.path)

    def test_failed_load_does_not_change_existing_collection(self):
        existing_tickets = [
            ticket.copy() for ticket in self.tickets
        ]

        self.path.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_tickets(self.path)

        self.assertEqual(self.tickets, existing_tickets)


if __name__ == "__main__":
    unittest.main()