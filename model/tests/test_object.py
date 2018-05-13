import unittest

from .. import ObjectParser as Subject

from . import abstract_test

CONFIG = {
    'property':{
        'map': 'newProperty'
    },
}

SOURCE = {
    'p1': 'hello',
    'newProperty': 'fuck you!'
}
API_DATA = {
    'p1': 'hello',
    'property': 'fuck you!'
}

ObjectParserTest = abstract_test(Subject, CONFIG, SOURCE, API_DATA)
