
from .collection import register_parser, parsers

@register_parser
class ArrayParser:
    def __init__(self, config):
        content = config.get('content', {})
        t= content.get('type', 'identity')
        content_config = content.get('config', {})
        self.content = parsers.get(t)(content_config)

    def serialize(self, data):
        return [
            self.content.serialize(v)
            for v in data
        ]

    def unserialize(self, data):
        return [
            self.content.unserialize(v)
            for v in data
        ]
