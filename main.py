#!/usr/bin/env python3
import argparse
import yaml
import sys
import os

from model import ModelService, ForeignKeyNotAvailableException
from auth import auth_methods

class BackupTool:
    def __init__(self, config, path):
        self.models_service = ModelService(config.get('server'), path)
        session = config.get('session')
        session_type = auth_methods.get(session.get('type'))
        self.session_manager = session_type(self.models_service, session)
        self.models_list = config.get('models')
        self.folder = config.get('folder')

    def backup(self):
        self.session_manager.authenticate()
        for name in self.models_list:
            sys.stdout.write('[{}]:'.format(name))
            sys.stdout.flush()

            model = self.models_service.get(name)
            sys.stdout.write('.')
            sys.stdout.flush()
            data = model.get_all()
            sys.stdout.write('.')
            sys.stdout.flush()
            with open(self.folder+'/'+name, 'w') as f:
                f.write(yaml.dump(data))
                print("ok")

    def restore(self):
        def create_or_true(model, data):
            try:
                model.create(data)
            except ForeignKeyNotAvailableException:
                return True
            return False

        self.session_manager.authenticate()
        data = {}
        for name in self.models_list:
            with open(self.folder+'/'+name, 'r') as f:
                data[name] = yaml.load(f.read())
        apply_changes = True
        while apply_changes:
            apply_changes = False
            for name in data.keys():
                model = self.models_service.get(name)
                l = data.get(name)
                new_l = [ e for e in l if create_or_true(model, e)]
                apply_changes = apply_changes or len(l) > len(new_l)
                data[name] = new_l
                
            data = {
                k: v
                for k, v in data.items()
                if len(v)>0
            }
        if len(data.keys())>0:
            print("pending data: \n{}".format(yaml.dump(data)))






def main():
    parser = argparse.ArgumentParser(description='Backup data from finances-server and restore using the api')
    parser.add_argument('config', help='The configuration file to connect')
    parser.add_argument('-r', '--restore', action='store_true', default=False)

    args = parser.parse_args()

    with open(args.config) as f:
        defaultConfig = yaml.load(f)
    
    backup = BackupTool(defaultConfig, os.path.dirname(os.path.abspath(args.config)))
    if not args.restore:
        backup.backup()
    else:
        backup.restore()

if __name__ == '__main__':
    main()