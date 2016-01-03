import queue
import time
import pdb


class Backtest(object):
    def __init__(self, quotes, instruments, data_handler, strategy, strategy_params, portfolio, execution, equity=10000,
                 heartbeat=0.0, max_iters=100000):
        self.instruments = instruments
        self.events_queue = queue.Queue()
        self.ticker = data_handler(quotes=quotes, event_queue=self.events_queue)
        self.strategy = strategy(self.instruments, self.events_queue, **strategy_params)
        self.equity = equity
        self.heartbeat = heartbeat
        self.max_iters = max_iters
        self.portfolio = portfolio
        self.execution = execution

    def start_backtest(self):
        print("Running backtest")
        iters = 0
        while iters < self.max_iters and not self.ticker.end_backtest:
            try:
                event = self.events_queue.get(block=False)
            except queue.Empty:
                self.ticker.stream_tick()
            else:
                if event is not None:
                    if event.event_type == 'TICK':
                        self.strategy.calc_signals(event)
                    elif event.event_type == 'SIGNAL':
                        self.execution.execute_signal(event)
                    elif event.event_type == 'ORDER':
                        self.execution.execute_order(event)

            time.sleep(self.heartbeat)
            iters += 1




