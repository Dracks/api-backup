
from model import parsers

class Model:
    def __init__(self, session, server, config):
        self.session = session
        self.server = server
        self.config = config
        self.endpoint = self.config.get('endpoint').get('name')
        self.fields = parsers.get('object')(config.get('model', {}))

    def create(self, data):
        send = self.fields.serialize(data)
        r =  self.session.post(self.server+self.endpoint+'/', json=send)
        if r.status_code == 201:
            return self.fields.unserialize(r.json())
        else:
            raise Exception(r.status_code)

    def get_all(self):
        r = self.session.get(self.server+self.endpoint+'/')
        if r.status_code == 200:
            f = self.fields
            return [ f.unserialize(e) for e in r.json()]
        else:
            raise Exception(r.status_code)
