from backtest import Backtest
from prices import FetchPrices, PricesFromDataFrame


# cont_1m = Quandl.get("CHRIS/CBOE_VX1", trim_start=trimstart)
# cont_2m = Quandl.get('CHRIS/CBOE_VX2', trim_start=trimstart)
# vix = Quandl.get('CBOE/VIX', trim_start=trimstart)

# l=list(df.columns.levels[0])

fetcher = FetchPrices()
names=['vxx', 'xiv']
qts = fetcher.get_quotes()

bt = Backtest(instruments=qts, data_handler=PricesFromDataFrame, strategy=TestStrategy, strategy_params=None,
              portfolio=None, execution=None)
bt.start_backtest()
