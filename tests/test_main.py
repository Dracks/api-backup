from unittest import TestCase
from unittest.mock import patch, Mock
import os
from io import StringIO

from main import BackupTool
from auth import RestCookie, auth_methods
from model import Model, ForeignKeyNotAvailableException

PATH = os.path.dirname(__file__)

BASE_CONFIG = {
    'server': 'mock://',
    'session': {
        'type': 'Type'
    },
    'models': [
        'simple'
    ],
    'folder': os.path.join(PATH,"data")
}

class BackupToolTest(TestCase):
    def patcher(self, name):
        p = patch(name)
        mock = p.start()
        self.addCleanup(p.stop)
        return mock

    def setUp(self):
        self.model_service_mock = self.patcher('model.ModelService')
        self.session_mock = Mock(spec = RestCookie)
        self.models_mock = {
            'simple': Mock(spec = Model)
        }
        with patch.dict(auth_methods, {'Type': lambda *args: self.session_mock}, clear=True):
            
            self.subject = BackupTool(BASE_CONFIG, '/path')
            self.subject.models_service = self.model_service_mock
    
        self.model_service_mock.get.side_effect=lambda m: self.models_mock.get(m)

    def test_wake_up_with_mock(self):
        self.assertTrue(isinstance(self.subject, BackupTool))

    def test_restore(self):
        self.models_mock.get('simple').create.side_effect=None
        self.subject.restore()
        self.session_mock.authenticate.assert_called_with()
        self.models_mock.get('simple').create.assert_any_call({"data":"ok3"})
        self.models_mock.get('simple').create.assert_any_call({"data":"ok"})
        self.models_mock.get('simple').create.assert_any_call({"data":"ok2"})

    def test_restore_with_references(self):
        self.models_mock.get('simple').create.side_effect=[ForeignKeyNotAvailableException, None, None, None]
        self.subject.restore()
        self.session_mock.authenticate.assert_called_with()
        self.models_mock.get('simple').create.assert_called_with({"data":"ok"})

    @patch('sys.stdout', new_callable=StringIO)
    def test_restore_with_references_but_not_complete(self, mock):
        self.models_mock.get('simple').create.side_effect=[ForeignKeyNotAvailableException, None, None, ForeignKeyNotAvailableException]
        self.subject.restore()
        self.session_mock.authenticate.assert_called_with()
        self.models_mock.get('simple').create.assert_called_with({"data":"ok"})
        #self.assertEquals(mock.getvalue(), 'pending data: \nsimple:\n- {data: ok}\n\n')