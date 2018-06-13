from .. import ForeignKeyParser as Subject
from .. import ForeignKeyNotAvailableException

from . import abstract_test

CONFIG = {
    'model': 'pepe'
}

SOURCE = 3

API_DATA = 3

FOREIGN_KEYS = {
    'pepe': {
        3: 5
    }
}

class ForeignKeyParserTest(abstract_test(Subject, CONFIG, SOURCE, API_DATA, FOREIGN_KEYS)):
    def test_serialize(self):
        data = self.subject.serialize(SOURCE)
        self.assertEquals(5, data)

    def test_launch_exception(self):
        try:
            self.subject.serialize(14)
            self.assertTrue(False)
        except ForeignKeyNotAvailableException:
            self.assertTrue(True)
