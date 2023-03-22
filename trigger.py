import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import scanner
from datetime import datetime


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print('event')
        scanner.main()
        observer.unschedule_all()
        observer.schedule(event_handler, path, recursive=True)
        time.sleep(60)
        scanner.main()



if __name__ == "__main__":
    path = "/home/parallels/Downloads/checking/"
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
