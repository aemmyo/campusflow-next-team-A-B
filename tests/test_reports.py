import unittest

from campusflow.reports import (
    get_ticket_summary,
    count_tickets_by_status,
    count_tickets_by_priority,
    count_tickets_by_category,
    count_assignment_status,
)


class TestTicketReports(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "critical",
                "category": "network",
                "assigned_to": "Felix",
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "high",
                "category": "hardware",
                "assigned_to": None,
            },
            {
                "id": "T003",
                "status": "open",
                "priority": "high",
                "category": "network",
                "assigned_to": "Grace",
            },
        ]

    def test_total_ticket_count(self):
        result = get_ticket_summary(self.tickets)

        self.assertEqual(result["total"], 3)

    def test_count_by_status(self):
        result = count_tickets_by_status(self.tickets)

        self.assertEqual(
            result,
            {"open": 2, "in_progress": 1},
        )

    def test_count_by_priority(self):
        result = count_tickets_by_priority(self.tickets)

        self.assertEqual(
            result,
            {"critical": 1, "high": 2},
        )

    def test_count_by_category(self):
        result = count_tickets_by_category(self.tickets)

        self.assertEqual(
            result,
            {"network": 2, "hardware": 1},
        )

    def test_count_assigned_and_unassigned(self):
        result = count_assignment_status(self.tickets)

        self.assertEqual(result["assigned"], 2)
        self.assertEqual(result["unassigned"], 1)

    def test_empty_ticket_list(self):
        self.assertEqual(get_ticket_summary([]), {"total": 0})
        self.assertEqual(count_tickets_by_status([]), {})
        self.assertEqual(count_tickets_by_priority([]), {})
        self.assertEqual(count_tickets_by_category([]), {})
        self.assertEqual(
            count_assignment_status([]),
            {"assigned": 0, "unassigned": 0},
        )


if __name__ == "__main__":
    unittest.main()