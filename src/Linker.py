try:
    import Queue as Q
except ImportError:
    import queue as Q

from multiprocessing import Process, Queue
import multiprocessing

from random import randint
import time

from globals import NB_ILOTS, ILOTS_LIST, PERCENTAGE_TRANSMISSION_STATS
from Message import Message


class Linker(object):
    instance_count = 0

    def __init__(self):
        self.queue = Queue()

        self.id = Linker.instance_count
        Linker.instance_count += 1

        self.queue_watcher = Process(target=self.reader)
        self.queue_watcher.start()

    def join(self):
        if self.queue_watcher:
            self._send(self.id, Message.Types.end)
            self.queue_watcher.join()

    def _send(self, id_receiver, type_message, data={}):
        message = Message(self.id, type_message, data)
        ILOTS_LIST[id_receiver].put_in_queue(message)

    def reader(self):

        while True:
            try:
                msg = self.queue.get_nowait()
                if msg.type == Message.Types.stat_transmission:
                    data = self.compare(msg.data)
                    self._send(msg.id_sender, Message.Types.answer, data)
                elif msg.type == Message.Types.answer:
                    self.process_answer(msg.data)
                else:
                    break
            except Q.Empty:
                pass

    def put_in_queue(self, stat):
        self.queue.put(stat)

    def send_statistics(self):
        if randint(0, 100) < PERCENTAGE_TRANSMISSION_STATS:
            id_receiver = self.id
            while id_receiver == self.id:
                id_receiver = randint(0, NB_ILOTS)

            self._send(1, Message.Types.stat_transmission, self.get_stats())

    def get_stats(self):
        pass

    def process_answer(self, data):
        pass

    def compare(self, stat):
        pass


class LinkerShell(Linker):
    """ Example of a child class of Linker """
    def __init__(self):
        # Values is a shared array of size 1
        # d is the type, you can all of them on https://docs.python.org/2/library/array.html#module-array
        self.values = multiprocessing.Array('d', 1)
        self.values[0] = 5

        super(self.__class__, self).__init__()

    def get_stats(self):
        """ Get the statistics of the object.

        :return: the statistics
        """
        return self.values[0]

    def process_answer(self, data):
        """ Process the data given back by another ilot.

        :param data: data given back by an ilot
        """
        self.values[0] += data

    def compare(self, stat):
        """ Get the stat given by another ilot, process it, then give back datas

        scenario:
        ilo1 --- get_stats() --> ilo2
        ilo1 <-- compare()   --- ilo2
        ilo1.process_answer()
        
        :param stat: statistics of the other ilot
        :return: data to process by the other
        """
        if stat > self.values[0]:
            self.values[0] -= 1
            return 1
        else:
            self.values[0] += 1
            return -1


if __name__ == '__main__':
    for i in xrange(NB_ILOTS):
        linker = LinkerShell()
        ILOTS_LIST.append(linker)

    for ii in xrange(0, 10):
        ILOTS_LIST[0].send_statistics()

    time.sleep(5)

    for i in xrange(NB_ILOTS):
        print(ILOTS_LIST[i].values[0])
        ILOTS_LIST[i].join()