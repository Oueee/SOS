try:
    import Queue as Q
except ImportError:
    import queue as Q

from multiprocessing import Process, Queue
import time

from threading import Thread
from random import randint
from os import sys, path
import time

from globals import NB_ILOTS, ILOTS_LIST
from Message import Message


class Linker(object):
    instance_count = 0

    def __init__(self):
        self.queue = Queue()

        self.id = Linker.instance_count
        Linker.instance_count += 1

        self.queue_watcher = Process(target=self.reader)
        self.queue_watcher.start()

    def delete(self):
        if self.queue_watcher:
            self.send(self.id, Message.Types.end)
            self.queue_watcher.join()

    def send(self, id_receiver, type_message, data={}):
        message = Message(self.id, type_message, data)
        ILOTS_LIST[id_receiver].put_in_queue(message)

    def reader(self):
    ## Read from the queue
        while True:
            try:
                msg = self.queue.get_nowait()        # Read from the queue and do nothing
                if (msg.type == Message.Types.end):
                    break
                else:
                    print(msg.data)
            except Q.Empty:
                pass

    def put_in_queue(self, stat):
        self.queue.put(stat)

    def join(self):
        self.queue_watcher.join()

#
#     def __run_queue_watcher(self):
#         while not self.to_terminate:
#             try:
#                 message = self.queue.get_nowait()
#                 print(message)
#                 if message.type == MessageType.stat_transmission:
#                     data = self.compare(message.data)
#                     ilot = ILOTS_LIST[message.id_sender]
#                     answer = Message(self.id, data, MessageType.answer)
#                     ilot.put_in_queue(answer)
#                 else:
#                     self.process_answer(message.data)
#
#                 self.queue.task_done()
#             except queue.Empty:
#                 pass
#
#     def send(self):
#         if randint(0, 100) > 100:
#             ilot = ILOTS_LIST[1]
#             message = Message(self.id, self.get_stats(),
#                               MessageType.stat_transmission)
#             ilot.put_in_queue(message)
#
#         print('message sent')
#
#     def get_stats(self):
#         pass
#
#     def process_answer(self, data):
#         pass
#
#     def compare(self, stat):
#         pass
#



if __name__=='__main__':
    for i in xrange(NB_ILOTS):
        linker = Linker()
        ILOTS_LIST.append(linker)

    for ii in xrange(0, 10):
        ILOTS_LIST[0].send(1, Message.Types.stat_transmission, ii)            # Write 'count' numbers into the queu

    for i in xrange(NB_ILOTS):
        ILOTS_LIST[i].delete()

# if __name__ == "__main__":
#     # for i in xrange(2):
#     #     linker = LinkerTest()
#     #     ILOTS_LIST.append(linker)
#     #
#     # ILOTS_LIST[0].send()
#     #
#     # time.sleep(2)
#     # for i in xrange(2):
#     #     ILOTS_LIST[i].delete()
#
