import json
import os
import yaml
import requests

from . import Model

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
            return Model(model, self.session, self.server, config)

    def get(self, model):
        m=self.__models.get(model, None)
        if m is None:
            m = self.__create_model(model)
            self.__models[model] = m
        return m