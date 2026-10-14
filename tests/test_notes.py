import unittest

from campusflow.tickets import (
    create_ticket,
    assign_ticket,
    change_status,
)
from campusflow.notes import (
    add_note,
    get_notes,
    next_note_id,
)


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = []

        self.ticket = create_ticket(
            self.tickets,
            "Wi-Fi is not working",
            "Network",
            "high",
            10,
        )

    def test_add_note(self):
        note = add_note(
            self.tickets,
            "T001",
            "Mentor A",
            "Router reboot attempted",
        )

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(
            note["message"],
            "Router reboot attempted",
        )

    def test_second_note_gets_next_id(self):
        add_note(
            self.tickets,
            "T001",
            "Mentor A",
            "Router reboot attempted",
        )

        note = add_note(
            self.tickets,
            "T001",
            "Mentor B",
            "Checking the network switch",
        )

        self.assertEqual(note["note_id"], "N002")

    def test_blank_author_rejected(self):
        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T001",
                "   ",
                "Router reboot attempted",
            )

        self.assertEqual(self.ticket["notes"], [])

    def test_short_message_rejected(self):
        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T001",
                "Mentor A",
                "No",
            )

        self.assertEqual(self.ticket["notes"], [])
        self.assertEqual(next_note_id(self.ticket), "N001")

    def test_long_message_rejected(self):
        message = "A" * 301

        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T001",
                "Mentor A",
                message,
            )

        self.assertEqual(self.ticket["notes"], [])
        self.assertEqual(next_note_id(self.ticket), "N001")

    def test_note_rejected_for_resolved_ticket(self):
        assign_ticket(self.tickets, "T001", "Mentor A")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T001",
                "Mentor A",
                "Router reboot attempted",
            )

        self.assertEqual(self.ticket["notes"], [])

    def test_note_allowed_after_reopening(self):
        assign_ticket(self.tickets, "T001", "Mentor A")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        change_status(self.tickets, "T001", "open")

        note = add_note(
            self.tickets,
            "T001",
            "Mentor B",
            "Checking the network switch",
        )

        self.assertEqual(note["note_id"], "N001")

    def test_existing_notes_preserved_after_resolve(self):
        add_note(
            self.tickets,
            "T001",
            "Mentor A",
            "Router reboot attempted",
        )

        assign_ticket(self.tickets, "T001", "Mentor A")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        self.assertEqual(len(self.ticket["notes"]), 1)
        self.assertEqual(
            self.ticket["notes"][0]["note_id"],
            "N001",
        )

    def test_get_notes_returns_notes_in_id_order(self):
        add_note(
            self.tickets,
            "T001",
            "Mentor A",
            "Router reboot attempted",
        )

        add_note(
            self.tickets,
            "T001",
            "Mentor B",
            "Checking the network switch",
        )

        notes = get_notes(self.tickets, "T001")

        self.assertEqual(
            [note["note_id"] for note in notes],
            ["N001", "N002"],
        )

    def test_invalid_ticket_rejected(self):
        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T999",
                "Mentor A",
                "Router reboot attempted",
            )


if __name__ == "__main__":
    unittest.main()