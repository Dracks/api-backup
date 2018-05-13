import json
import os
import yaml
import requests

class LambdaParser:
    def __init__(self, key, config):
        self.key = key

    def serialize(self, obj, data):
        key = self.key
        obj[key] = data[key]

    def unserialize(self, obj, data):
        key = self.key
        obj[key] = data[key]


class IgnoreParser:
    def __init__(self, key, config):
        self.key = key

    def serialize(self, obj, data):
        del obj[self.key]

    def unserialize(self, obj, data):
        del obj[self.key]


class PropertyParser:
    def __init__(self, key, config):
        self.key = key
        self.value = config.get('value')

    def serialize(self, obj, data):
        obj[self.key] = data.get(self.value, None)

    def unserialize(self, obj, data):
        obj[self.value] = data.get(self.key, None)

class ForeigKeyParser(LambdaParser):
    def __init__(self, key, config):
        super(ForeigKeyParser, self).__init__(key, config)
        self.model_transform = config.get('model')

    def serialize(self, obj, data):
        raise Exception('Not Implemented')

class ArrayParser(LambdaParser):
    def __init__(self, key, config):
        super(ArrayParser, self).__init__(key, config)
        self.contents_config = config.get('contents')
        self.contents = hashProperty[self.contents_config.get('type')]

    def serialize(self, obj, data):
        data = data.get(self.key,[])
        l = len(data)
        r = [None]*l
        for key in range(l):
            self.contents(key, self.contents_config).serialize(r, data)
        return r
    
    def unserialize(self, obj, data):
        data = data.get(self.key, [])
        l = len(data)
        r = [None]*l
        for key in range(l):
            self.contents(key, self.contents_config).unserialize(r, data)
        return r

hashProperty ={
    "ignore": IgnoreParser,
    "property": PropertyParser,
    "foreign_key": ForeigKeyParser,
    "array": ArrayParser,
}
class FieldsParser:
    def __init__(self, model):
        self.model = {}
        for key in model.keys():
            m = model.get(key)
            self.model[key]= hashProperty.get(m.get('type'))(key, m)

    def serialize(self, data):
        r = { }
        for key in data.keys():
            LambdaParser(key, None).serialize(r, data)

        for key in self.model.keys():
            self.model[key].serialize(r, data)

        return r

    def unserialize(self, data):
        r = {}

        for key in data.keys():
            LambdaParser(key, None).unserialize(r, data)

        for key in self.model.keys():
            self.model[key].unserialize(r, data)

        return r

class Model:
    def __init__(self, session, server, config):
        self.session = session
        self.server = server
        self.config = config
        self.endpoint = self.config.get('endpoint').get('name')
        self.fields = FieldsParser(config.get('model', {}))

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
    def __init__(self, server):
        self.__models = {}
        self.session = requests.Session()
        self.server = server

    def __create_model(self, model):
        p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'models',model+'.yml')
        with open(p) as f:
            config = yaml.load(f)
            return Model(self.session, self.server, config)

    
    def get(self, model):
        m=self.__models.get(model, None)
        if m is None:
            m = self.__create_model(model)
            self.__models[model] = m
        return m