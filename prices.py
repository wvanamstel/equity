import pandas as pd
import numpy as np
import Quandl

from decimal import Decimal, getcontext, ROUND_HALF_DOWN
from datetime import date
from events import Tick
from cql.cluster import CqlClient
from cql.models import *
from settings.cf_mapping import symbol_cf_map

getcontext().rounding = ROUND_HALF_DOWN

class Prices(object):
    def _price_structure(self):
        quotes = dict(
            (k, v) for k, v in [
                (p, {"Close": None}) for p in self.instruments
                ]
        )

        return quotes


class PricesFromDataFrame(Prices):
    def __init__(self, event_queue, quotes):
        """
        Handle prices from pandas data frames
        :param event_queue: event queue
        :param quotes: dict of pandas dataframes with quotes of instruments
        :return:
        """
        self.instruments = quotes.keys()
        self.end_backtest = False
        self.ticker_cursor = pd.concat(quotes.values()).sort().iterrows()
        self.tick_dict = {'time': None, 'bid': None, 'ask': None}
        self.event_queue = event_queue

    def stream_tick(self):
        try:
            time_stamp, row = next(self.ticker_cursor)
        except StopIteration:
            self.end_backtest = True
            return

        name = row['Name']
        close_price = row['Close']

        tick_event = Tick(instrument=name, time_stamp=time_stamp, bid=close_price, ask=close_price)

        self.event_queue.put(tick_event)


class FetchPrices(object):
    def __init__(self, instruments=None, start_date='2015-01-01', end_date=date.today().isoformat()):
        if instruments is not None:
            self.names = instruments
        else:
            self.names = ['vxx', 'xiv']
        self.start_date = start_date
        self.end_date = end_date

    def get_quotes(self):
        quotes = {}
        for name in self.names:
            name = name.upper()
            quandl_format = 'GOOG/NYSEARCA_' + name
            quotes[name] = Quandl.get(quandl_format, trim_start=self.start_date, trim_end=self.end_date)
            quotes[name]['Name'] = name

        return quotes


class FetchCassPrices(object):
    def __init__(self, instruments, events_queue=None):
        self.quotes = dict()
        self.generator = None
        self.continue_backtest = True
        self.events_queue = events_queue
        self.instruments = instruments
        self.current_prices = {key: dict() for key in instruments}

    def get_quotes(self, start_date, end_date):
        # TODO: add possibility to query from various column families; map symbol --> CF? then no need to pass CF
        CqlClient(symbol_cf_map[self.instruments[0]])
        for instr in self.instruments:
            query = symbol_cf_map[instr].objects.limit(None).filter(ticker=instr, date__gte=start_date, date__lte=end_date)
            cols = query.first().keys()
            df = pd.DataFrame(columns=cols)
            df = df.append([dict(row) for row in query.all()])
            df.index = df["time"]
            del df["date"]
            self.quotes[instr] = df
        self.generator = self.get_generator()

    def get_generator(self):
        # Find common intersecting index
        df_index = self.quotes[self.instruments[0]].index
        for symbol in self.instruments:
            df_index = self.quotes[symbol].index.intersection(df_index)

        # Reindex to common, dropna
        for symbol in self.instruments:
            self.quotes[symbol] = self.quotes[symbol].reindex(df_index).dropna()

        # Concatenate
        return pd.concat(self.quotes.values()).sort_index().iterrows()

    def stream_tick(self):
        try:
            index, row = self.generator.__next__()
        except StopIteration:
            self.continue_backtest = False
            return None

        ticker = row["ticker"]
        close = row["close"]
        bid = Decimal(str(close)).quantize(
            Decimal("0.00001")
        )
        ask = Decimal(str(close)).quantize(
            Decimal("0.00001")
        )

        # Create decimalised prices for traded pair
        self.current_prices[ticker]["bid"] = bid
        self.current_prices[ticker]["ask"] = ask
        self.current_prices[ticker]["timestamp"] = index

        # Create the tick event for the queue
        tick_event = Tick(instrument=ticker, bid=bid, ask=ask, time_stamp=index)
        self.events_queue.put(tick_event)

