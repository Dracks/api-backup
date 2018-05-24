from unittest.mock import patch
from unittest import TestCase
import requests_mock
import os

from .. import ModelService

PATH = os.path.dirname(__file__)

class ModelIntegrationTest(TestCase):
    def setUp(self):
        self.subject = ModelService('mock://server', PATH)
        self.adapter = requests_mock.Adapter()
        self.subject.session.mount('mock', self.adapter)

    def test_get_simple_model(self):
        obj = self.subject.get('simple')
        self.assertIsNotNone(obj)
        self.assertEqual(obj.endpoint, 'mock://server/simple/')

    def test_get_all_simple_model(self):
        obj = self.subject.get('simple')
        self.adapter.register_uri('GET', obj.endpoint, text='[{"fuck":"data"}]')
        data = obj.get_all()
        self.assertEquals(len(data),1)
        self.assertEquals(data, [{"fuck":"data"}])

    


    