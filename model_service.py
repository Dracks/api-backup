import json
import os
import yaml
import requests

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

class ModelService:
    def __init__(self, server, path):
        self.__models = {}
        self.session = requests.Session()
        self.server = server
        self.path = path

    def __create_model(self, model):
        p=os.path.join(self.path,'models',model+'.yml')
        with open(p) as f:
            config = yaml.load(f)
            return Model(self.session, self.server, config)

    
    def get(self, model):
        m=self.__models.get(model, None)
        if m is None:
            m = self.__create_model(model)
            self.__models[model] = m
        return m