import unittest
from io import StringIO
from unittest.mock import patch

from campusflow.quiz import calculate_score, run_quiz
from campusflow.quiz_questions import QUESTIONS


class TestQuiz(unittest.TestCase):

    def test_all_correct_answers(self):
        answers = [question["answer"] for question in QUESTIONS]
        self.assertEqual(calculate_score(answers), 6)

    def test_all_wrong_answers(self):
        answers = ["A" if q["answer"] != "A" else "B" for q in QUESTIONS]
        self.assertEqual(calculate_score(answers), 0)

    def test_lowercase_answers_are_accepted_for_scoring(self):
        answers = [question["answer"].lower() for question in QUESTIONS]
        self.assertEqual(calculate_score(answers), 6)

    def test_empty_answers_score_zero(self):
        self.assertEqual(calculate_score([]), 0)

    @patch(
        "builtins.input",
        side_effect=[
            "B",
            "C", "The empty collection must be handled safely.",
            "B",
            "C",
            "C", "Duplicate IDs must be rejected.",
            "B",
        ],
    )
    def test_results_are_shown_after_all_six_questions(self, mock_input):
        output = StringIO()

        with patch("sys.stdout", output):
            run_quiz()

        result = output.getvalue()
        self.assertEqual(result.count("Correct answer:"), 6)
        self.assertGreater(
            result.index("Correct answer:"),
            result.index("Question 6:"),
        )
        self.assertIn("Your score: 6/6", result)


if __name__ == "__main__":
    unittest.main()
