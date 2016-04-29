import pandas as pd
import numpy as np
import Quandl

from decimal import Decimal, getcontext, ROUND_HALF_DOWN
from datetime import date
from events import Tick
from cql.cluster import CqlClient
from cql.models import *

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
    def __init__(self, events_queue=None):
        self.quotes = dict()
        self.generator = None
        self.continue_backtest = True
        self.events_queue = events_queue

    def get_quotes(self, instruments, model, start_date, end_date):
        CqlClient(model)
        for instr in instruments:
            query = model.objects.limit(None).filter(ticker=instr, date__gte=start_date, date__lte=end_date)
            cols = query.first().keys()
            df = pd.DataFrame(columns=cols)
            df = df.append([dict(row) for row in query.all()])
            df.index = df["time"]
            del df["date"]
            self.quotes[instr] = df
        self.generator = self.get_generator()

    def get_generator(self):
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
        # self.tickers[ticker]["bid"] = bid
        # self.tickers[ticker]["ask"] = ask
        # self.tickers[ticker]["timestamp"] = index

        # Create the tick event for the queue
        tick_event = Tick(ticker, index, bid, ask)
        self.events_queue.put(tick_event)



fcp=FetchCassPrices()
fcp.get_quotes(["wti", "brent"], FuturesMins, "2016-01-05", "2016-01-12")
it = fcp.get_iterator()

