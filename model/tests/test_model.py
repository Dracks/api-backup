from unittest.mock import patch
from unittest import TestCase
import requests_mock
import os
import json

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

    def test_post_all_simple_model(self):
        obj = self.subject.get('simple')
        self.adapter.register_uri('POST', obj.endpoint, status_code=201, text='{"fuck":"data"}')
        newData = obj.create({"ping":"pong"})
        self.assertEquals({"ping": "pong"}, json.loads(self.adapter.last_request.body))
        self.assertEquals({"fuck":"data"}, newData)


    