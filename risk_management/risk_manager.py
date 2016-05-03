from events import Order

class RiskManager(object):
    def __init__(self):
        pass

    def check_orders(self, portfolio, prelim_order_sized):
        order_event = Order(time_stamp=prelim_order_sized.time_stamp, instrument=prelim_order_sized.instrument,
                            side=prelim_order_sized.side, size=prelim_order_sized.size, order_type=prelim_order_sized.order)
        return [order_event]
