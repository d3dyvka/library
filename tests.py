import unittest
from unittest.mock import patch, mock_open
import json
from io import StringIO
from main import load_file, add, delete, search, update_status, display


class TestLibraryFunctions(unittest.TestCase):

    def setUp(self):
        self.sample_data = [
            {"id": 1, "title": "Война и мир", "author": "Лев Толстой", "year": 1869, "status": "в наличии"},
            {"id": 2, "title": "1984", "author": "Джордж Оруэлл", "year": 1949, "status": "выдана"}
        ]
        self.mock_file_name = 'library'

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "title": "Война и мир", "author": "Лев Толстой", "year": 1869, "status": "в наличии"},
        {"id": 2, "title": "1984", "author": "Джордж Оруэлл", "year": 1949, "status": "выдана"}
    ]))
    def test_load_file(self, mock_file):
        data = load_file(self.mock_file_name)
        self.assertEqual(data, self.sample_data)
        mock_file.assert_called_with('library.json', 'r')

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.input", side_effect=["Мастер и Маргарита", "Михаил Булгаков", "1967"])
    def test_add(self, mock_input, mock_file):
        data = self.sample_data[:]
        add(data, self.mock_file_name)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[-1], {
            "id": 3,
            "title": "Мастер и Маргарита",
            "author": "Михаил Булгаков",
            "year": 1967,
            "status": "в наличии"
        })

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.input", side_effect=["1"])
    def test_delete(self, mock_input, mock_file):
        data = self.sample_data[:]
        delete(data, self.mock_file_name)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 2)

    @patch("builtins.input", side_effect=["2", "1984"])
    def test_search_by_title(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            search(self.sample_data)
            output = fake_out.getvalue().strip()
        self.assertIn('"1984"', output)

    @patch("builtins.input", side_effect=["3", "Лев Толстой"])
    def test_search_by_author(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            search(self.sample_data)
            output = fake_out.getvalue().strip()
        self.assertIn('"Война и мир"', output)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.input", side_effect=["2", "в наличии"])
    def test_update_status(self, mock_input, mock_file):
        data = self.sample_data[:]
        update_status(data, self.mock_file_name)
        self.assertEqual(data[1]['status'], "в наличии")

    @patch("builtins.input", side_effect=["4"])
    def test_invalid_search_criterion(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            search(self.sample_data)
            output = fake_out.getvalue().strip()
        self.assertIn("Некорректный выбор", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display(self, mock_stdout):
        display(self.sample_data)
        output = mock_stdout.getvalue().strip()
        self.assertIn('"Война и мир"', output)
        self.assertIn('"1984"', output)


if __name__ == "__main__":
    unittest.main()
