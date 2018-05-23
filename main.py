#!/usr/bin/env python3
import argparse
import yaml
import sys
import os

from model import ModelService
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