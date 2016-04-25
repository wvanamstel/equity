import datetime as dt
import numpy as np
import pandas as pd

# from abc import ABCMeta, abstractmethod
from math import floor

from events import Fill, Order


class SimplePortfolio(object):
    def __init__(self, events_queue):
        self.events_queue = events_queue

    def update_signal(self):
        pass

    def generate_simple_order(self, signal):
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength

        # mkt_quantity = floor(100 * strength)
        # cur_quantity = self.current_positions[symbol]
        # order_type = 'MKT'

        # if direction == 'LONG' and cur_quantity == 0:
        #     order = Order(symbol, order_type, mkt_quantity, 'BUY')
        # if direction == 'SHORT' and cur_quantity == 0:
        #     order = Order(symbol, order_type, mkt_quantity, 'SELL')

        # if direction == 'EXIT' and cur_quantity > 0:
        #     order = Order(symbol, order_type, abs(cur_quantity), 'SELL')
        # if direction == 'EXIT' and cur_quantity < 0:
        #     order = Order(symbol, order_type, abs(cur_quantity), 'BUY')
        return order