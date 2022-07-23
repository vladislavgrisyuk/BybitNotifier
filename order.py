class order:
    def __init__(self, symbol, side, entryPrice, createdAt, leverage):
        self.symbol = symbol
        self.side = side
        self.entryPrice = entryPrice
        self.createdAt = createdAt
        self.leverage = leverage
