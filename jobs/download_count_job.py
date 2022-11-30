# Updated download count statistics

import time
from datetime import datetime, timedelta
from hashlib import md5
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyNginxHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_modified = datetime.now()

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
            with open('./test_watch_dog/app.access.log', 'r') as nginx_log:
                lines = nginx_log.read().split('\n')
                for line in lines:
                    print(line)
                    print(md5(line.encode()).hexdigest())


if __name__ == "__main__":
    event_handler = MyNginxHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./test_watch_dog', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
