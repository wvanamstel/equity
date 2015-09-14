class Tick(object):
    def __init__(self, instrument, bid, ask, close, time_stamp):
        self.instrument = instrument
        self.bid = bid
        self.ask = ask
        self.close = close
        self.time_stamp = time_stamp
        self.event_type = 'TICK'

    def __str__(self):
        out = 'Time: {}, Event: {}, Instrument: {}, Bid: {}, Ask: {}, Close: {}'.format(str(self.time_stamp),
                                                                                   str(self.event_type),
                                                                                   str(self.instrument),
                                                                                   str(self.bid),
                                                                                   str(self.ask),
                                                                                   str(self.close),
                                                                                   )
        return out

    def __repr__(self):
        return str(self)


class Signal(object):
    def __init__(self, instrument, order, side, time_stamp):
        self.instrument = instrument
        self.order = order
        self.side = side
        self.time_stamp = time_stamp
        self.event_type = 'SIGNAL'

    def __str__(self):
        out = 'Time: {}, Event: {}, Side: {}, Order: {}, Instrument: {}'.format(str(self.time_stamp),
                                                                                      str(self.event_type),
                                                                                      str(self.side),
                                                                                      str(self.order),
                                                                                      str(self.instrument),
                                                                                      )
        return out

    def __repr__(self):
        return str(self)


class Order(object):
    def __init__(self, instrument, order, size, side, time_stamp):
        self.instrument = instrument
        self.order = order
        self.size = size
        self.side = side
        self.time_stamp = time_stamp
        self.event_type = 'ORDER'

    def __str__(self):
        out = 'Time: {}, Event: {}, Side: {}, Size: {}, Order: {}, Instrument: {}'.format(str(self.time_stamp),
                                                                                                  str(self.event_type),
                                                                                                  str(self.side),
                                                                                                  str(self.size),
                                                                                                  str(self.order),
                                                                                                  str(self.instrument),
                                                                                                  )
        return out

    def __repr__(self):
        return str(self)
