import queue
import time
import pdb

from decimal import Decimal


class Backtest(object):
    def __init__(self, instruments, data_handler, dates, strategy, strategy_params, portfolio_handler, execution,
                 order_sizer, risk_manager, cash=Decimal(10000.00), heartbeat=0.0, max_iters=10):
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
                        self.portfolio_handler.handle_signal(event)
                    elif event.event_type == 'ORDER':
                        self.execution.execute_order(event)
                    elif event.event_type == "FILL":
                        self.portfolio_handler.handle_fill(event)

            time.sleep(self.heartbeat)
            iters += 1




