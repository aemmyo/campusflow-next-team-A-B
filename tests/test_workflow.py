import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_ticket_status


class TestTicketAssignment(unittest.TestCase):

    def setUp(self):
        self.tickets = []

        create_ticket(
            self.tickets,
            "Internet is down",
            "network",
            "high",
            5,
        )

    def test_assign_ticket_successfully(self):
        ticket = assign_ticket(self.tickets, "T001", "Felix")

        self.assertEqual(ticket["assigned_to"], "Felix")
        self.assertEqual(ticket["id"], "T001")

    def test_assign_ticket_strips_staff_name(self):
        ticket = assign_ticket(self.tickets, "T001", "  Felix  ")

        self.assertEqual(ticket["assigned_to"], "Felix")

    def test_assign_unknown_ticket_raises_error(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Felix")

    def test_blank_staff_name_raises_error(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_non_string_staff_name_raises_error(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", 123)

    def test_resolved_ticket_cannot_be_reassigned(self):
        # Assign the ticket before starting work.
        assign_ticket(self.tickets, "T001", "Felix")

        update_ticket_status(self.tickets, "T001", "in_progress")
        update_ticket_status(self.tickets, "T001", "resolved")

        original_assignee = self.tickets[0]["assigned_to"]

        # Reassignment must fail for a resolved ticket.
        with self.assertRaises(ValueError):
            assign_ticket(
                self.tickets,
                "T001",
                "Another Staff Member",
            )

        # The failed operation must not change the assignment.
        self.assertEqual(
            self.tickets[0]["assigned_to"],
            original_assignee,
        )

    def test_resolved_ticket_can_be_reassigned_after_reopening(self):
        assign_ticket(self.tickets, "T001", "Felix")

        update_ticket_status(self.tickets, "T001", "in_progress")
        update_ticket_status(self.tickets, "T001", "resolved")
        update_ticket_status(self.tickets, "T001", "open")

        ticket = assign_ticket(
            self.tickets,
            "T001",
            "Another Staff Member",
        )

        self.assertEqual(
            ticket["assigned_to"],
            "Another Staff Member",
        )


class TestTicketStatusWorkflow(unittest.TestCase):

    def setUp(self):
        self.tickets = []

        create_ticket(
            self.tickets,
            "Internet is down",
            "network",
            "high",
            5,
        )

        assign_ticket(self.tickets, "T001", "Felix")

    def test_open_ticket_moves_to_in_progress(self):
        ticket = update_ticket_status(
            self.tickets, "T001", "in_progress"
        )

        self.assertEqual(ticket["status"], "in_progress")

    def test_in_progress_ticket_moves_to_resolved(self):
        update_ticket_status(self.tickets, "T001", "in_progress")

        ticket = update_ticket_status(
            self.tickets, "T001", "resolved"
        )

        self.assertEqual(ticket["status"], "resolved")

    def test_in_progress_ticket_can_return_to_open(self):
        update_ticket_status(self.tickets, "T001", "in_progress")

        ticket = update_ticket_status(
            self.tickets, "T001", "open"
        )

        self.assertEqual(ticket["status"], "open")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "pending")

    def test_invalid_transition_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        update_ticket_status(self.tickets, "T001", "in_progress")
        update_ticket_status(self.tickets, "T001", "resolved")

        ticket = update_ticket_status(
            self.tickets, "T001", "open"
        )

        self.assertEqual(ticket["status"], "open")

    def test_resolved_ticket_cannot_restart_directly(self):
        update_ticket_status(self.tickets, "T001", "in_progress")
        update_ticket_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            update_ticket_status(
                self.tickets, "T001", "in_progress"
            )

    def test_unassigned_ticket_cannot_start_work(self):
        tickets = []

        create_ticket(
            tickets,
            "Printer is not working",
            "hardware",
            "medium",
            2,
        )

        with self.assertRaises(ValueError):
            update_ticket_status(tickets, "T001", "in_progress")

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(
                self.tickets, "T999", "in_progress"
            )

    def test_status_is_case_insensitive(self):
        ticket = update_ticket_status(
            self.tickets, "T001", "IN_PROGRESS"
        )

        self.assertEqual(ticket["status"], "in_progress")


if __name__ == "__main__":
    unittest.main()