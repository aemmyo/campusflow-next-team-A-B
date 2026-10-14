import unittest

from campusflow.validation import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    validate_assignment,
    calculate_priority,
    validate_ticket_id,
    validate_note_id,
)


class TestValidation(unittest.TestCase):

    # Title tests
    def test_valid_title(self):
        validate_title("Wi-Fi is not working")

    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    # Category tests
    def test_valid_category(self):
        validate_category("Network")

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            validate_category("Electricity")

    # Urgency tests
    def test_valid_urgency(self):
        validate_urgency("high")

    def test_invalid_urgency_rejected(self):
        with self.assertRaises(ValueError):
            validate_urgency("urgent")

    # Affected-user tests
    def test_valid_affected_users(self):
        validate_affected_users(10)

    def test_zero_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_negative_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-1)

    def test_float_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(2.5)

    def test_boolean_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users(True)

    def test_string_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_affected_users("10")

    # Assignment tests
    def test_valid_assignment(self):
        validate_assignment("Mentor A")

    def test_blank_assignment_rejected(self):
        with self.assertRaises(ValueError):
            validate_assignment("   ")

    # Priority tests
    def test_critical_priority(self):
        self.assertEqual(
            calculate_priority("high", 10),
            "critical",
        )

    def test_high_priority(self):
        self.assertEqual(
            calculate_priority("high", 3),
            "high",
        )

    def test_medium_priority(self):
        self.assertEqual(
            calculate_priority("medium", 3),
            "medium",
        )

    def test_low_priority(self):
        self.assertEqual(
            calculate_priority("low", 1),
            "low",
        )

    # ID tests
    def test_valid_ticket_id(self):
        validate_ticket_id("T001")

    def test_invalid_ticket_id(self):
        with self.assertRaises(ValueError):
            validate_ticket_id("ABC")

    def test_valid_note_id(self):
        validate_note_id("N001")

    def test_invalid_note_id(self):
        with self.assertRaises(ValueError):
            validate_note_id("NOTE")


if __name__ == "__main__":
    unittest.main()