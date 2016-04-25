import pandas as pd
import numpy as np
import Quandl

from datetime import date
from events import Tick
from cql.cluster import CqlClient
from cql.models import *


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
    def __init__(self, instruments, model, start_date, end_date=date.today()):
        self.model = model
        self.instruments = instruments
        self.start_date = start_date
        self.end_date = end_date
        self.connection = CqlClient(self.model)
        # self.connection.connect()

    def get_quotes(self):
        out = list()
        for instr in self.instruments:
            query = self.model.objects.limit(None).filter(forex_pair=instr, date__gte=self.start_date,
                                                          date__lte=self.end_date)
            cols = query.first().keys()
            df = pd.DataFrame(columns=cols)
            df = df.append([dict(row) for row in query.all()])
            out.append(df)
        return out

