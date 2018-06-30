
from .collection import register_parser
from .identity import Identity
from .exceptions import ForeignKeyNotAvailableException, NotWellConfiguredException

@register_parser("foreign_key")
class ForeignKeyParser(Identity):
    def __init__(self, config, fk):
        model = config.get('model')
        
        if not model:
            raise NotWellConfiguredException(-1, 'Model not configured on foreign_key')
        f = fk.get(model, None)
        
        if f is None:
            self.fk = {}
            fk[model] = self.fk
        else:
            self.fk = f

    def serialize(self, data):
        v = None
        if data is not None:
            v = self.fk.get(data,None)
            if not v:
                raise ForeignKeyNotAvailableException()
        return v