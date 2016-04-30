from decimal import Decimal

from backtest import Backtest
from execution import SimExecution
from portfolio import SimplePortfolio
# from position_sizer import PositionSizer


from strategy import Test
from prices import FetchCassPrices


if __name__ == "__main__":
    instruments = ['brent', "wti"]
    strategy_params = {"division": 5}
    fetch_prices = FetchCassPrices(instruments)
    prices = fetch_prices.get_quotes()

    backtest = Backtest(
        instruments=instruments,
        data_handler=FetchCassPrices,
        strategy=Test,
        strategy_params=strategy_params,
        portfolio="niets",
        execution=SimExecution
    )

    backtest.start_backtest()