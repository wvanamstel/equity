import queue
import time
import os
import datetime as dt
from decimal import Decimal

from settings import settings

class Backtest(object):
    def __init__(self, instruments, data_handler, dates, strategy, strategy_params, portfolio_handler, execution,
                 order_sizer, risk_manager, cash=Decimal(10000.00), heartbeat=0.0, max_iters=1000000000):
        self.equity_dir = settings.OUTPUT_DIR
        self.equity_file = os.path.join(self.equity_dir, "equity.csv")
        self.events_queue = queue.Queue()
        self.instruments = instruments
        self.quote_data = data_handler(instruments, events_queue=self.events_queue, **dates)
        self.strategy = strategy(self.instruments, self.events_queue, **strategy_params)
        self.cash = cash
        self.heartbeat = heartbeat
        self.max_iters = max_iters
        self.execution = execution(self.events_queue, self.quote_data)
        self.order_sizer = order_sizer()
        self.risk_manager = risk_manager()
        self.portfolio_handler = portfolio_handler(cash=self.cash, events_queue=self.events_queue,
                                                   quote_data=self.quote_data, order_sizer=self.order_sizer,
                                                   risk_manager=self.risk_manager)
        self.current_time = None

        # Ugly hack to clear file for each backtest run
        # TODO: write logic to have some sort of unique identifyer for each backtest run
        open(self.equity_file, "w").close()

    def start_backtest(self):
        print("Running backtest")
        iters = 0
        ticks = 0
        while iters < self.max_iters and self.quote_data.continue_backtest:
            try:
                event = self.events_queue.get(block=False)
            except queue.Empty:
                self.quote_data.stream_tick()
            else:
                if event is not None:
                    if event.event_type == 'TICK':
                        self.current_time = event.time_stamp
                        self._append_equity_state()
                        self.strategy.calc_signals(event)
                        self.portfolio_handler.update_portfolio_value()
                        ticks += 1
                        if ticks % 100 == 0:
                            print(event)
                    elif event.event_type == 'SIGNAL':
                        print(event)
                        self.portfolio_handler.handle_signal(event)
                    elif event.event_type == 'ORDER':
                        print(event)
                        self.execution.execute_order(event)
                    elif event.event_type == "FILL":
                        print(event)
                        self.portfolio_handler.handle_fill(event)

            time.sleep(self.heartbeat)
            iters += 1

    def _append_equity_state(self):
        cur_port_state = self.portfolio_handler.portfolio.create_portfolio_state_dict()
        with open(self.equity_file, "a") as eqfile:
            eqfile.write(
                "%s,%s\n" % (
                    self.current_time, cur_port_state["equity"]
                )
            )



