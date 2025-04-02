class StockNotFoundError(Exception):
    def __init__(self, symbol: str):
        super().__init__(f"Stock '{symbol}' not found.")


class InvalidTradeTypeError(Exception):
    def __init__(self, trade_type: str):
        super().__init__(f"Invalid trade type: '{trade_type}'. Must be 'buy' or 'sell'.")
