
from .collection import register_parser, parsers
from .identity import Identity


identity = Identity()

@register_parser
class ObjectParser():
    def __init__(self, config, fk):
        self.map = {}
        self.keys_map = {}
        self.keys_reverse = {}
        for key, c in config.items():
            map_key = c.get('map')
            if map_key is not None:
                self.keys_map[key]= map_key
                self.keys_reverse[map_key] = key
            t = c.get('type')
            if t is not None:
                self.map[key] = parsers.get(t)(c, fk)
    
    def serialize(self, data):
        return {
            self.keys_reverse.get(key, key): self.map.get(key, identity).serialize(value)
            for key, value in data.items()
        }

    def unserialize(self, data):
        return {
            self.keys_map.get(key, key): self.map.get(key, identity).unserialize(value)
            for key, value in data.items()
        }
    