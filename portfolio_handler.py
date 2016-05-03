import datetime as dt
import numpy as np
import pandas as pd

from math import floor

from events import Fill, Order


class PortfolioHandler(object):
    def __init__(self, events_queue, equity, quote_data, order_sizer, risk_manager):
        self.events_queue = events_queue
        self.equity = equity
        self.quote_data = quote_data
        self.order_sizer = order_sizer
        self.risk_manager = risk_manager
        # self.portfolio = Portfolio(quote_data, equity)
        self.portfolio = None

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

    def _prelim_order_from_signal(self, signal_event):
        return PrelimOrder(signal_event.instrument, signal_event.side)

    def _put_orders_on_queue(self, order_events):
        for order in order_events:
            self.events_queue.put(order)

    def handle_signal(self, signal_event):
        prelim_order = self._prelim_order_from_signal(signal_event)
        prelim_order_sized = self.order_sizer.size_order(prelim_order)
        order_events = self.risk_manager.check_orders(self.portfolio, prelim_order_sized)
        self._put_orders_on_queue(order_events)

    def handle_fill(self, fill_event):
        self.update_portfolio(fill_event)

    def update_portfolio(self, fill_event):
        side = fill_event.side
        instrument = fill_event.instrument
        size = fill_event.size
        price = fill_event.price
        commission = fill_event.commission

        # Create or modify the position from the fill info
        self.portfolio.transact_position(side, instrument, size, price, commission)

class PrelimOrder(object):
    def __init__(self, instrument, side, size=0):
        self.instrument=instrument
        self.side=side
        self.size=size