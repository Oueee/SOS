import multiprocessing
import random


def f(vector):
    return random.randint(0, 100)

NB_ILOTS = multiprocessing.cpu_count()
ILOTS_LIST = []
PERCENTAGE_TRANSMISSION_STATS = 10