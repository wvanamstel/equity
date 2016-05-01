import queue
import time
import pdb

from decimal import Decimal


class Backtest(object):
    def __init__(self, instruments, data_handler, dates, strategy, strategy_params, portfolio_handler, execution,
                 position_sizer, risk_manager=None, equity=Decimal(10000.00), heartbeat=0.0, max_iters=10):
        self.events_queue = queue.Queue()
        self.instruments = instruments
        self.quote_data = data_handler(instruments, events_queue=self.events_queue, **dates)
        self.strategy = strategy(self.instruments, self.events_queue, **strategy_params)
        self.equity = equity
        self.heartbeat = heartbeat
        self.max_iters = max_iters
        self.execution = execution(self.events_queue)
        self.position_sizer = position_sizer()
        # self.risk_manager = risk_manager()
        self.portfolio = portfolio_handler(self.equity, self.events_queue, self.quote_data, self.position_sizer) #self.risk_manager)

    def start_backtest(self):
        print("Running backtest")
        iters = 0
        while iters < self.max_iters and self.quote_data.continue_backtest:
            try:
                event = self.events_queue.get(block=False)
            except queue.Empty:
                self.quote_data.stream_tick()
            else:
                if event is not None:
                    if event.event_type == 'TICK':
                        self.strategy.calc_signals(event)
                    elif event.event_type == 'SIGNAL':
                        self.portfolio.handle_signal(event)
                    elif event.event_type == 'ORDER':
                        self.execution.execute_order(event)

            time.sleep(self.heartbeat)
            iters += 1




