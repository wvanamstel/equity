import datetime as dt
import queue

from abc import ABCMeta, abstractmethod

from events import Fill, Order


class ExecutionHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError


class SimExecution(ExecutionHandler):
    def __init__(self, events_queue):
        self.events_queue = events_queue

    def execute_order(self, event):
        if event.event_type == "ORDER":
            fill_event = Fill(dt.datetime.utcnow(), event.symbol, event.quantity, event.side, event.price)
            self.events_queue.put(fill_event)
