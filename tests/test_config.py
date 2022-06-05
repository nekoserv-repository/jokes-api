import os
import unittest
from io import StringIO
from unittest.mock import patch

from config.configservice import ConfigService


class TestConfig(unittest.TestCase):
    mock_os_env = {
        'API_BASE_URL': 'mock API_BASE_URL',
        'API_PORT': 'mock API_PORT',
        'JSON_FILE_PATH': 'mock JSON_FILE_PATH'
    }

    @patch.dict(os.environ, mock_os_env, clear=True)
    def test_check_runtime_cfg_all_env_vars_are_set(self):
        for e in self.mock_os_env.keys():
            ConfigService.get(e)

    @patch.dict(os.environ, {
        'API_BASE_URL': 'a',
        'API_PORT': 'b'}, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_runtime_cfg_missing_at_least_one_env_var(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            for e in self.mock_os_env.keys():
                ConfigService.get(e)
        self.assertEqual(context.exception.code, 1)
        self.assertEqual('runtime parameter "JSON_FILE_PATH" is not set\n', mock_stdout.getvalue())

    @patch.dict(os.environ, {}, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_runtime_cfg_missing_all_env_vars(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            for e in self.mock_os_env.keys():
                ConfigService.get(e)
        self.assertEqual(context.exception.code, 1)
        self.assertEqual('runtime parameter "JSON_FILE_PATH" is not set\n', mock_stdout.getvalue())

    @patch.dict(os.environ, {'JSON_FILE_PATH': 'a'}, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_runtime_cfg_default_values(self, mock_stdout):
        for e in self.mock_os_env.keys():
            ConfigService.get(e)
        self.assertEqual('/', ConfigService.get('API_BASE_URL'))
        self.assertEqual(5000, ConfigService.get('API_PORT'))
