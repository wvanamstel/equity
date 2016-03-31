import datetime as dt
import numpy as np
import pandas as pd
import random

from abc import ABCMeta, abstractmethod

from events import Signal


class Strategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calc_signals(self):
        raise NotImplementedError


class Test(Strategy):
    def __init__(self, instrument, events_queue, division):
        self.name = instrument
        self.events_queue = events_queue

    def calc_signals(self):
        if random.random() > 0.5:
            signal = Signal(self.name, "market", "buy", event.time_stamp)
            self.events_queue.put(signal)


class SimpleSpread(Strategy):
    def __init__(self, instruments, events_queue):
        self.instr_1 = instruments.iloc[:0]
        self.instr_2 = instruments.iloc[:1]
        self.events_queue = events_queue

    def calc_signals(self):
