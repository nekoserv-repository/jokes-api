import os
from importlib import resources
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, MagicMock, ANY

from tools.jsonmngr import JsonMngr


class TestJsonMngr(TestCase):
    json_sample = resources.files('tests').joinpath('resources/sample.json').as_posix()
    jm = None
    joke_1 = {'id': 1, 'type': 'cat1', 'joke': 'joke1', 'answer': 'answer1'}
    joke_2 = {'id': 2, 'type': 'cat2', 'joke': 'joke2', 'answer': 'answer2'}
    categories = {'categories': ['cat1', 'cat2']}

    def setUp(self):
        self.jm = JsonMngr()

    @patch.dict(os.environ, {'JSON_FILE_PATH': json_sample}, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_data(self, mock_stdout):
        self.jm.load_data()
        self.assertEqual('> loading JSON file... done\n', mock_stdout.getvalue())
        self.assertEqual(2, self.jm.nb_jokes)

    @patch.dict(os.environ, {'JSON_FILE_PATH': './does_not_exists'}, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_data_file_not_found(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            self.jm.load_data()
        self.assertEqual(context.exception.code, 1)
        self.assertEqual('json file not found : "./does_not_exists"\n', mock_stdout.getvalue())

    @patch.dict(os.environ, {'JSON_FILE_PATH': 'dummy'}, clear=True)
    @patch('tools.jsonmngr.open', MagicMock(return_value=ANY))
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_data_other_except(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            self.jm.load_data()
        self.assertEqual(context.exception.code, 1)
        self.assertEqual('can\'t open json file : "dummy"\n', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test__categorizing(self, mock_stdout):
        self.jm.json_data = [self.joke_1, self.joke_2]
        self.jm._categorizing()
        self.assertEqual('> loading JSON file... done\n', mock_stdout.getvalue())
        self.assertEqual({'cat1': [self.joke_1], 'cat2': [self.joke_2]},
                         self.jm.json_data_categorized)

    def test_get_random_joke(self):
        self.jm.nb_jokes = 2
        self.jm.json_data = [self.joke_1, self.joke_2]
        joke = self.jm.get_random_joke()
        self.assertTrue(joke == self.joke_1 or self.joke_2)

    def test_get_random_joke_empty(self):
        joke = self.jm.get_random_joke_with_type('don_t_care')
        self.assertIsNone(joke)

    def test_get_random_joke_with_type(self):
        self.jm.json_data = [self.joke_1, self.joke_2]
        self.jm._categorizing()
        joke = self.jm.get_random_joke_with_type('cat1')
        self.assertTrue(joke == self.joke_1)

    def test_get_random_joke_with_type_invalid_cat(self):
        self.jm.json_data = [self.joke_1, self.joke_2]
        self.jm._categorizing()
        joke = self.jm.get_random_joke_with_type('invalid_cat')
        self.assertIsNone(joke)

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_categories(self, mock_stdout):
        self.jm.json_data = [self.joke_1, self.joke_2]
        self.jm._categorizing()
        categories = self.jm.get_categories()
        self.assertEqual(self.categories, categories)
        self.assertEqual('> loading JSON file... done\n', mock_stdout.getvalue())
