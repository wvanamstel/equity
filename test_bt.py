
from backtest import Backtest
from execution import SimExecution
# from qsforex.portfolio.portfolio import Portfolio
from strategy import Test
from prices import PricesFromDataFrame, FetchPrices


if __name__ == "__main__":
    instruments = ['vxx']
    strategy_params = {"division": 5}
    fetch_prices = FetchPrices(instruments)
    prices = fetch_prices.get_quotes()

    backtest = Backtest(
        quotes=prices,
        instruments=instruments,
        data_handler=PricesFromDataFrame,
        strategy=Test,
        strategy_params=strategy_params,
        portfolio="niets",
        execution=SimExecution
    )

    backtest.start_backtest()