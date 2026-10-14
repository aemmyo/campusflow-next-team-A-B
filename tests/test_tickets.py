import unittest

from campusflow.tickets import (
    create_ticket,
    assign_ticket,
    change_status,
    find_ticket,
    next_ticket_id,
)


class TestTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = []

        self.ticket = create_ticket(
            self.tickets,
            "Wi-Fi is not working",
            "Network",
            "high",
            10,
        )

    def test_create_ticket(self):
        self.assertEqual(self.ticket["id"], "T001")
        self.assertEqual(self.ticket["title"], "Wi-Fi is not working")
        self.assertEqual(self.ticket["category"], "Network")
        self.assertEqual(self.ticket["status"], "open")
        self.assertIsNone(self.ticket["assigned_to"])
        self.assertEqual(self.ticket["notes"], [])

    def test_ticket_priority(self):
        self.assertEqual(self.ticket["priority"], "critical")

    def test_next_ticket_id(self):
        create_ticket(
            self.tickets,
            "Laptop problem",
            "Hardware",
            "medium",
            3,
        )

        self.assertEqual(next_ticket_id(self.tickets), "T003")

    def test_invalid_ticket_not_created(self):
        original = [ticket.copy() for ticket in self.tickets]

        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets,
                "",
                "Network",
                "high",
                10,
            )

        self.assertEqual(self.tickets, original)

    def test_assign_ticket(self):
        assign_ticket(
            self.tickets,
            "T001",
            "Mentor A",
        )

        self.assertEqual(
            self.ticket["assigned_to"],
            "Mentor A",
        )

    def test_blank_assignee_rejected(self):
        original = self.ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(
                self.tickets,
                "T001",
                "   ",
            )

        self.assertEqual(self.ticket, original)

    def test_unassigned_ticket_cannot_start(self):
        original = self.ticket.copy()

        with self.assertRaises(ValueError):
            change_status(
                self.tickets,
                "T001",
                "in_progress",
            )

        self.assertEqual(self.ticket, original)

    def test_assigned_ticket_can_start(self):
        assign_ticket(self.tickets, "T001", "Mentor A")

        change_status(
            self.tickets,
            "T001",
            "in_progress",
        )

        self.assertEqual(self.ticket["status"], "in_progress")

    def test_in_progress_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, "T001", "Mentor A")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        self.assertEqual(self.ticket["status"], "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        assign_ticket(self.tickets, "T001", "Mentor A")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        change_status(self.tickets, "T001", "open")

        self.assertEqual(self.ticket["status"], "open")

    def test_resolved_ticket_cannot_be_reassigned(self):
        assign_ticket(self.tickets, "T001", "Mentor A")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        original = self.ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Mentor B")

        self.assertEqual(self.ticket, original)

    def test_invalid_status_rejected(self):
        original = self.ticket.copy()

        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "cancelled")

        self.assertEqual(self.ticket, original)

    def test_missing_ticket_rejected(self):
        with self.assertRaises(ValueError):
            find_ticket(self.tickets, "T999")


if __name__ == "__main__":
    unittest.main()