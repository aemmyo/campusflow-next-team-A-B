import unittest

from campusflow.queue import (
    get_open_tickets,
    get_assigned_tickets,
    sort_tickets_by_priority,
)


class TestTicketQueue(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "low",
                "assigned_to": "Felix",
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "critical",
                "assigned_to": "Grace",
            },
            {
                "id": "T003",
                "status": "open",
                "priority": "high",
                "assigned_to": "Felix",
            },
        ]

    def test_get_open_tickets(self):
        result = get_open_tickets(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T003"],
        )

    def test_get_assigned_tickets(self):
        result = get_assigned_tickets(self.tickets, "Felix")

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T003"],
        )

    def test_assigned_tickets_ignore_case(self):
        result = get_assigned_tickets(self.tickets, "felix")

        self.assertEqual(len(result), 2)

    def test_blank_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            get_assigned_tickets(self.tickets, "   ")

    def test_sort_by_priority(self):
        result = sort_tickets_by_priority(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T002", "T003", "T001"],
        )

    def test_sort_does_not_modify_original_list(self):
        original_ids = [
            ticket["id"] for ticket in self.tickets
        ]

        sort_tickets_by_priority(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )


if __name__ == "__main__":
    unittest.main()