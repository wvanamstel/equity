import queue
import time
import pdb

class Backtest(object):
    def __init__(self, instruments, data_handler, strategy, strategy_params, portfolio, execution, equity=10000,
                 heartbeat=0.0, max_iters=100000):
        self.instruments = instruments
        self.events = queue.Queue()
        self.ticker = data_handler(quotes=self.instruments, event_queue=self.events)
        # self.strategy = strategy(self.instruments, self.events, **strategy_params)
        self.equity = equity
        self.heartbeat = heartbeat
        self.max_iters = max_iters
        # self.portfolio =
        # self.execution = execution()

    def start_backtest(self):
        # pdb.set_trace()
        iters = 0
        while iters < self.max_iters and not self.ticker.end_backtest:
            try:
                event = self.events.get(block=False)
            except queue.Empty:
                self.ticker.stream_tick()
            else:
                if event is not None:
                    if event.event_type == 'TICK':
                        print(event)
            time.sleep(self.heartbeat)
            iters += 1




