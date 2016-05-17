try:
    import Queue as queue
except ImportError:
    import queue

from threading import Thread
from .globals import NB_ILOTS, ILOTS_LIST
from random import randint


class Linker:
    def __init__(self):
        self.queue = queue.Queue(maxsize=10)
        self.to_terminate = False
        self.queue_watcher = Thread(target=self.__run_queue_watcher)
        self.queue_watcher.start()

    def __del__(self):
        self.to_terminate = True
        if self.queue_watcher:
            self.queue_watcher.join()

    def put_in_queue(self, stat):
        self.queue.put_nowait(stat)

    def __run_queue_watcher(self):
        while not self.to_terminate:
            stats = self.queue.get()
            self.compare(stats)
            self.queue.task_done()

    def send(self):
        if randint(0,100) > 10:
            ilot = ILOTS_LIST[randint(0, NB_ILOTS)]
            ilot.put_in_queue(self.get_stats())

    def get_stats(self):
        return {}

    def compare(self, stat):
        pass
