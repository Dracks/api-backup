
from .collection import register_parser
from .identity import Identity

@register_parser("foreign_key")
class ForeignKeyParser(Identity):
    pass