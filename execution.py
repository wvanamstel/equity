import datetime as dt
import queue

from decimal import Decimal
from abc import ABCMeta, abstractmethod

from events import Fill, Order


class ExecutionHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError


class SimExecution(ExecutionHandler):
    def __init__(self, events_queue, quote_data):
        self.events_queue = events_queue
        self.quote_data = quote_data

    def execute_order(self, event):
        if event.event_type == "ORDER":
            timestamp = dt.datetime.utcnow()
            instrument = event.instrument
            side = event.side
            size = event.size

            # Obtain the fill price
            bid, ask = self.quote_data.get_best_bid_ask(instrument)
            if event.action == "BOT":
                fill_price = Decimal(str(ask))
            else:
                fill_price = Decimal(str(bid))

            # Set a dummy exchange and calculate trade commission
            exchange = "BATS"
            commission = self.calculate_commission()

            # Create the FillEvent and place on the events queue
            fill_event = Fill(timestamp, instrument, side, size, exchange, fill_price, commission)
            self.events_queue.put(fill_event)

    def calculate_commission(self):
        return Decimal("1.00")

