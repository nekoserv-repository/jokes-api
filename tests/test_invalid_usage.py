from unittest import TestCase

from tools.invalid_usage import InvalidUsage


class TestInvalidUsage(TestCase):
    default_status_code = 400

    def test_constructor_with_message(self):
        iu = InvalidUsage('message')
        self.assertEqual('message', iu.message)
        self.assertEqual(self.default_status_code, iu.status_code)
        self.assertEqual(None, iu.payload)

    def test_constructor_with_message_and_code(self):
        iu = InvalidUsage('message1', status_code=1)
        self.assertEqual('message1', iu.message)
        self.assertEqual(1, iu.status_code)
        self.assertEqual(None, iu.payload)

    def test_constructor_with_message_and_payload(self):
        iu = InvalidUsage('message2', payload='payload1')
        self.assertEqual('message2', iu.message)
        self.assertEqual(self.default_status_code, iu.status_code)
        self.assertEqual('payload1', iu.payload)

    def test_constructor_with_message_and_code_and_payload(self):
        iu = InvalidUsage('message3', status_code=2, payload='payload2')
        self.assertEqual('message3', iu.message)
        self.assertEqual(2, iu.status_code)
        self.assertEqual('payload2', iu.payload)

    def test_to_dict_empty_payload(self):
        iu = InvalidUsage('message4')
        r = iu.to_dict()
        self.assertEqual({'message': 'message4'}, r)

    def test_to_dict_with_payload(self):
        iu = InvalidUsage('message5', payload={'a': 1})
        r = iu.to_dict()
        self.assertEqual({'a': 1, 'message': 'message5'}, r)

    def test_to_dict_with_payload_and_code(self):
        iu = InvalidUsage('message6', status_code=1, payload={'a': 2})
        r = iu.to_dict()
        self.assertEqual({'a': 2, 'message': 'message6'}, r)
