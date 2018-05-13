
import unittest 

from .. import parsers as subject

def abstract_test(Subject, config, source, api_data):
    class AbstractParserTest(unittest.TestCase):
        def setUp(self):
            self.subject = Subject(config)

        def test_serialize(self):
            data = self.subject.serialize(source)
            self.assertEqual(api_data, data)

        def test_unserialize(self):
            data = self.subject.unserialize(api_data)
            self.assertEqual(source, data)
    return AbstractParserTest

class RegisteringTest(unittest.TestCase):
    def test_register_object(self):
        s = subject.get('object')
        self.assertIsNotNone(s)
        self.assertIsNotNone(s({}))

    def test_register_array(self):
        s = subject.get('array')
        self.assertIsNotNone(s)

    def test_register_foreign_key(self):
        s = subject.get('foreign_key')
        self.assertIsNotNone(s)
