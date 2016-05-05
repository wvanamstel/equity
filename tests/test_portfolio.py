from decimal import Decimal
from portfolio.portfolio import Portfolio


class Quotes(object):
    @staticmethod
    def get_best_bid_ask(self, instrument):
        nbbo = {"abc": {"bid": Decimal("101.46"), "ask": Decimal("101.77")},
                "xyz": {"bid": Decimal("33.72"), "ask": Decimal("33.75")},
                }
        return nbbo[instrument]


class TestPortfolio(object):
    @classmethod
    def setup(cls):
        cls.quotes = Quotes()
        cls.initial_cash = Decimal("10000.00")
        cls.portfolio = Portfolio(cls.quotes, cls.initial_cash)

    def test_portfolio_object(self):
        assert self.portfolio.cur_cash == self.initial_cash
