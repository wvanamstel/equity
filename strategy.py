from events import Signal

class Test(object):
    def __init__(self, events):
        self.name = events.instrument
        self.events = events

    def calc_signals(self):
        pass
