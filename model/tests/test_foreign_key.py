from .. import ForeignKeyParser as Subject
from .. import ForeignKeyNotAvailableException

from . import abstract_test

CONFIG = {
    'model': 'pepe'
}

SOURCE = 3

API_DATA = 3


class ForeignKeyParserTest(abstract_test(Subject, CONFIG, SOURCE, API_DATA)):
    def setUp(self):
        self.fk={}
        self.subject = Subject(CONFIG, self.fk)

    def test_serialize(self):
        self.fk['pepe'][3]=5
        data = self.subject.serialize(SOURCE)
        self.assertEquals(5, data)

    def test_serializer_2(self):
        self.fk['pepe'] = {}
        subject = Subject(CONFIG, self.fk)
        self.fk['pepe'][3] = 5
        data = subject.serialize(SOURCE)
        self.assertEquals(5,data)

    def test_serialize_null(self):
        data = self.subject.serialize(None)
        self.assertIsNone(data)

    def test_launch_exception(self):
        try:
            self.subject.serialize(14)
            self.assertTrue(False)
        except ForeignKeyNotAvailableException:
            self.assertTrue(True)
