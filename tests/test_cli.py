import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

import main


class TestCampusFlowCLI(unittest.TestCase):

    @patch("builtins.input", side_effect=["15", "12"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_menu_choice(self, mock_output, mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "tickets.json")

            with patch("main.DATA_FILE", test_file):
                main.main()

        output = mock_output.getvalue()
        self.assertIn("Invalid menu choice", output)
        self.assertIn("1 to 12", output)

    @patch("builtins.input", side_effect=["12"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_save_and_exit(self, mock_output, mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "tickets.json")

            with patch("main.DATA_FILE", test_file):
                main.main()

        self.assertIn("Saved", mock_output.getvalue())


if __name__ == "__main__":
    unittest.main()
