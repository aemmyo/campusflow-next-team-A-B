import unittest

from campusflow.search import (
    search_tickets,
    sort_search_results_by_priority,
)


class TestTicketSearch(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T003",
                "title": "Network connection failed",
                "category": "network",
                "priority": "critical",
                "status": "in_progress",
                "assigned_to": "David",
            },
            {
                "id": "T001",
                "title": "Printer is not working",
                "category": "hardware",
                "priority": "medium",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Printer driver problem",
                "category": "software",
                "priority": "high",
                "status": "resolved",
                "assigned_to": "Mary",
            },
            {
                "id": "T004",
                "title": "Office computer is slow",
                "category": "hardware",
                "priority": "low",
                "status": "open",
                "assigned_to": None,
            },
        ]

    def test_search_title_ignores_case(self):
        results = search_tickets(self.tickets, title="PRINTER")

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T002"],
        )

    def test_search_title_supports_partial_text(self):
        results = search_tickets(self.tickets, title="driver")

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T002"],
        )

    def test_filter_by_category(self):
        results = search_tickets(self.tickets, category="hardware")

        self.assertEqual(
            {ticket["id"] for ticket in results},
            {"T001", "T004"},
        )

    def test_filter_by_status(self):
        results = search_tickets(self.tickets, status="open")

        self.assertEqual(
            {ticket["id"] for ticket in results},
            {"T001", "T004"},
        )

    def test_filter_by_priority(self):
        results = search_tickets(self.tickets, priority="critical")

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T003"],
        )

    def test_filters_are_combined(self):
        results = search_tickets(
            self.tickets,
            title="printer",
            category="software",
            status="resolved",
            priority="high",
        )

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T002"],
        )

    def test_empty_filters_return_all_tickets(self):
        results = search_tickets(self.tickets)

        self.assertEqual(len(results), 4)

    def test_no_matches_return_empty_list(self):
        results = search_tickets(self.tickets, title="mobile phone")

        self.assertEqual(results, [])

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category="food")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status="pending")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, priority="urgent")

    def test_non_string_title_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, title=123)

    def test_non_string_category_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, category=[])

    def test_non_string_status_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status=123)

    def test_non_string_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, priority=123)

    def test_search_does_not_modify_original_list(self):
        original_ids = [ticket["id"] for ticket in self.tickets]

        search_tickets(self.tickets, category="hardware")

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )

    def test_sort_by_priority_and_numeric_id(self):
        results = sort_search_results_by_priority(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T003", "T002", "T001", "T004"],
        )

    def test_sort_does_not_modify_original_list(self):
        original_ids = [ticket["id"] for ticket in self.tickets]

        sort_search_results_by_priority(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in self.tickets],
            original_ids,
        )


if __name__ == "__main__":
    unittest.main()
