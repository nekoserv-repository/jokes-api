import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from jokes_api import api
from jokes_api import get_joke, get_joke_with_type, handle_404, handle_invalid_usage
from tests.test_jsonmngr import TestJsonMngr
from tools.invalid_usage import InvalidUsage


class TestJokesApi(TestCase):
    invalid_usage = InvalidUsage('Nothing jokes here', status_code=500)
    test_client = None

    def setUp(self):
        api.config['JSON_SORT_KEYS'] = False
        self.test_client = api.test_client()

    @patch('tools.jsonmngr.JsonMngr.get_random_joke', MagicMock(return_value=TestJsonMngr.joke_1))
    def test_get_joke(self):
        r = self.test_client.get('/joke/random')
        actual = json.loads(r.data)
        self.assertEqual(TestJsonMngr.joke_1, actual)

    @patch('tools.jsonmngr.JsonMngr.get_random_joke', MagicMock(return_value=None))
    def test_get_joke_empty(self):
        with self.assertRaises(InvalidUsage):
            get_joke()

    @patch('tools.jsonmngr.JsonMngr.get_random_joke_with_type', MagicMock(return_value=TestJsonMngr.joke_1))
    def test_get_joke_with_type(self):
        r = self.test_client.get('/joke/type/dummy')
        actual = json.loads(r.data)
        self.assertEqual(TestJsonMngr.joke_1, actual)

    @patch('tools.jsonmngr.JsonMngr.get_random_joke_with_type', MagicMock(return_value=None))
    def test_get_joke_with_type_empty(self):
        with self.assertRaises(InvalidUsage):
            get_joke_with_type('dummy')

    @patch('tools.jsonmngr.JsonMngr.get_categories', MagicMock(return_value=TestJsonMngr.categories))
    def test_get_categories(self):
        r = self.test_client.get('/joke/type/list')
        actual = json.loads(r.data)
        self.assertEqual(TestJsonMngr.categories, actual)

    def test_handle_404(self):
        error = handle_404('test')
        self.assertEqual({'message': 'Not found', 'status_code': 404}, error)

    def test_handle_invalid_usage(self):
        ia = InvalidUsage(message='testing')
        invalid_usage_error = handle_invalid_usage(ia)
        self.assertEqual({'message': 'testing', 'status_code': 400}, invalid_usage_error)
