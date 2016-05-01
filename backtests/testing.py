from decimal import Decimal

from backtest import Backtest
from execution import SimExecution
from portfolio import SimplePortfolio
# from position_sizer import PositionSizer


from strategy import Test
from prices import FetchCassPrices


if __name__ == "__main__":
    instruments = ['brent', "wti"]
    dates = {'start_date': "2016-01-01",
             "end_date": "2016-01-08"}
    strategy_params = {"division": 5}

    backtest = Backtest(
        instruments=instruments,
        data_handler=FetchCassPrices,
        dates=dates,
        strategy=Test,
        strategy_params=strategy_params,
        portfolio="niets",
        execution=SimExecution,
    )

    backtest.start_backtest()