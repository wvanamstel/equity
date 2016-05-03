class Event(object):
    pass


class Tick(Event):
    def __init__(self, instrument, bid, ask, time_stamp):
        self.instrument = instrument
        self.bid = bid
        self.ask = ask
        self.time_stamp = time_stamp
        self.event_type = 'TICK'

    def __str__(self):
        out = 'Time: {}, Event: {}, Instrument: {}, Bid: {}, Ask: {}'.format(str(self.time_stamp),
                                                                             str(self.event_type),
                                                                             str(self.instrument),
                                                                             str(self.bid),
                                                                             str(self.ask),
                                                                             )
        return out

    def __repr__(self):
        return str(self)


class Signal(Event):
    def __init__(self, instrument, order, side, time_stamp):
        self.instrument = instrument
        self.order = order
        self.side = side  # buy/sell
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


class Order(Event):
    def __init__(self, instrument, size, side):
        self.instrument = instrument
        self.size = size
        self.side = side
        self.event_type = 'ORDER'

    def __str__(self):
        out = 'Event: {}, Side: {}, Size:, Instrument: {}'.format(
            str(self.event_type),
            str(self.side),
            str(self.size),
            str(self.instrument),
        )
        return out

    def __repr__(self):
        return str(self)


class Fill(Event):
    def __init__(self, time_stamp, instrument, size, side, price, exchange, commission):
        self.time_stamp= time_stamp
        self.event_type = "FILL"
        self.instrument = instrument
        self.size = size
        self.side = side
        self.price = price
        self.commission = commission
        self.exchange = exchange

    def __str__(self):
        out = "Time: {}, Event: {}, Side:{}, Size: {}, Instrument: {}, Price: {}, Commission: {}".format(str(self.time_stamp),
                                                                                                         str(self.event_type),
                                                                                                         str(self.side),
                                                                                                         str(self.size),
                                                                                                         str(self.instrument),
                                                                                                         str(self.price),
                                                                                                         str(self.commission),
                                                                                                         )
        return out

    def __repr__(self):
        return str(self)

