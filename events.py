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

class Fill(Event):
    def __init__(self, time_stamp, symbol, quantity, side, price):
        self.time_stamp= time_stamp
        self.event_type = "FILL"
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.price = price

    def __str__(self):
        out = "Time: {}, Event: {}, Side:{}, Order: {}, Instrument: {}, Quantity: {}, Price: {}".format(str(self.event_type),
                                                                                                        str(self.event_type),
                                                                                                        str(self.side),
                                                                                                        str(self.symbol),
                                                                                                        str(self.quantity),
                                                                                                        str(self.price),
                                                                                                        )
    def __repr__(self):
        return str(self)

