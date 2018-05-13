from .collection import register_parser

@register_parser
class Identity():
    def __init__(self, config=None):
        pass

    def serialize(self, data):
        return data

    def unserialize(self, data):
        return data