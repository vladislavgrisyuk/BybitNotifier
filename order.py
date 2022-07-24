class order:
    def __init__(self, symbol, side, entryPrice, createdAt, leverage, order_id=-1, is_created=True):
        self.symbol = symbol
        self.side = side
        self.entryPrice = entryPrice
        self.createdAt = createdAt
        self.leverage = leverage
        self.order_id = order_id
        self.is_created = is_created
