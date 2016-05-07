from decimal import Decimal
from portfolio.portfolio import Portfolio


class Quotes(object):
    def get_best_bid_ask(self, instrument):
        nbbo = {"abc": {"bid": Decimal("101.46"), "ask": Decimal("101.77")},
                "xyz": {"bid": Decimal("33.72"), "ask": Decimal("33.75")},
                }
        return nbbo[instrument]["bid"], nbbo[instrument]["ask"]


class TestPortfolio(object):
    @classmethod
    def setup(cls):
        cls.quotes = Quotes()
        cls.initial_cash = Decimal("100000.00")
        cls.portfolio = Portfolio(cls.quotes, cls.initial_cash)
        cls.commission = Decimal("5.00")

    def test_init_portfolio_object(self):
        assert self.portfolio.cur_cash == self.initial_cash
        assert self.portfolio.init_cash == self.initial_cash
        assert self.portfolio.positions == {}
        assert self.portfolio.realised_pnl == Decimal("0.0")
        assert self.portfolio.unrealised_pnl == Decimal("0.0")

    def test_commission_accounting(self):
        self.setup()  # clear portfolio positions from previous tests
        self.portfolio.transact_position("buy", "abc", 100, Decimal("103.33"), self.commission)
        self.portfolio.transact_position("sell", "abc", 100, Decimal("103.33"), self.commission)
        assert self.portfolio.cur_cash == self.initial_cash - 2 * self.commission
        assert self.portfolio.realised_pnl == -2 * self.commission
        assert self.portfolio.unrealised_pnl == Decimal("0.00")

    def test_portfolio_transactions(self):
        self.setup()
        self.portfolio.transact_position("buy", "abc", 100, Decimal("103.33"), self.commission)
        self.portfolio.transact_position("buy", "abc", 150, Decimal("102.775"), self.commission)
        self.portfolio.transact_position("sell", "abc", 50, Decimal("104.08"), self.commission)
        self.portfolio.transact_position("buy", "xyz", 200, Decimal("33.67"), self.commission)
        self.portfolio.transact_position("sell", "xyz", 100, Decimal("33.55"), self.commission)
        self.portfolio.transact_position("sell", "xyz", 100, Decimal("34.448"), self.commission)
        assert self.portfolio.cur_cash == Decimal("79520.55") - 6 * self.commission
        assert self.portfolio.realised_pnl == Decimal("-41.65")


pt=TestPortfolio()
pt.test_portfolio_transactions()
