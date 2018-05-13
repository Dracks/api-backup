
from .collection import register_parser
from .identity import Identity

@register_parser
class IgnoreParser(Identity):
    def serialize(self, v):
        return None
    def unserialize(self, v):
        return None