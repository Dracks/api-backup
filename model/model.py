
from model import parsers

class Model:
    def __init__(self, name, session, server, fk, config):
        self.name = name
        self.session = session
        self.server = server
        self.config = config
        self.endpoint = server+self.config.get('endpoint', {}).get('name', "/"+name)+'/'
        self.fields = parsers.get('object')(config.get('model', {}), fk)
        #print(fk)
        self.fk = fk.get(name, None)
        if self.fk is None:
            fk[name] = self.fk = {}

    def create(self, data):
        send = self.fields.serialize(data)
        r =  self.session.post(self.endpoint, json=send)
        if r.status_code == 201:
            new_data = self.fields.unserialize(r.json())
            old_id = data.get('id', None)
            new_id = new_data.get('id', None)
            if old_id is not None and new_id is not None:
                self.fk[old_id] = new_id
            return new_data
        else:
            raise Exception(r.status_code, r.text)

    def get_all(self):
        r = self.session.get(self.endpoint)
        if r.status_code == 200:
            f = self.fields
            return [ f.unserialize(e) for e in r.json()]
        else:
            raise Exception(r.status_code)
