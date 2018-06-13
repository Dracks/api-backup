
from .collection import register_parser
from .identity import Identity
from .foreign_key_not_available import ForeignKeyNotAvailableException

@register_parser("foreign_key")
class ForeignKeyParser(Identity):
    def __init__(self, config, fk):
        model = config.get('model')
        f = fk.get(model, None)
        if not f:
            self.fk = {}
            fk[model]=self.fk
        else:
            self.fk = f

    def serialize(self, data):
        v = self.fk.get(data,None)
        if not v:
            raise ForeignKeyNotAvailableException()
        return v