import unittest

from .. import ArrayParser as Subject
from . import abstract_test

config = {
        'type': 'identity'
    }
ArrayParserTest = abstract_test(Subject, config, [1,2,3], [1,2,3])

config = {
    'content':{
        'type': 'object',
        'config':{
            'property':{
                'map': 'new'
            }
        }
    }
}
ArrayParserTest2 = abstract_test(Subject, config, [{'new':'hi'}], [{'property':'hi'}])


