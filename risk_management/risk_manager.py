from events import Order

class RiskManager(object):
    def __init__(self):
        pass

    def check_orders(self, portfolio, prelim_order_sized):
        order_event = Order(instrument=prelim_order_sized.instrument, side=prelim_order_sized.side, size=prelim_order_sized.size)
        return [order_event]