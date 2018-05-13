import argparse
import unittest
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def run():
    tests = unittest.TestLoader().discover(".")
    unittest.TextTestRunner().run(tests)

class RunTestsHandler(FileSystemEventHandler):
    def on_any_event(self, e):
        print(e)
        run()

def watch():
    path='.'
    observer = Observer()
    observer.schedule(RunTestsHandler(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup data from finances-server and restore using the api')
    parser.add_argument('-w', '--watch', action='store_true', default=False)
    
    args = parser.parse_args()
    run()
    if args.watch:
        watch()