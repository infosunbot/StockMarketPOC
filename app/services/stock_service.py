from datetime import datetime, timedelta
from app.data.stocks_data import stocks, trades_by_symbol
from app.models.trade import Trade
from app.models.enums import TradeType
from app.exceptions import StockNotFoundError, InvalidTradeTypeError
import math
import logging
from collections import deque
#from app.config import settings

logger = logging.getLogger(__name__)

async def calculate_dividend_yield(symbol: str, price: float) -> dict:
    """
    Calculate the dividend yield for a given stock symbol and market price.

    Args:
        symbol (str): The stock symbol to calculate for.
        price (float): The market price of the stock.

    Returns:
        dict: A dictionary containing the dividend yield (e.g., {"dividend_yield": float}).

    Raises:
        StockNotFoundError: If the symbol does not exist.
        ValueError: If the price is less than or equal to zero.
    """
    stock = stocks.get(symbol.upper())
    if not stock:
        raise StockNotFoundError(symbol)
    if price <= 0:
        raise ValueError("Price must be greater than zero")

    if stock['type'] == 'Common':
        return {"dividend_yield": stock['last_dividend'] / price}
    elif stock['type'] == 'Preferred':
        return {"dividend_yield": (stock['fixed_dividend'] * stock['par_value']) / price}

async def calculate_pe_ratio(symbol: str, price: float) -> dict:

    """
    Calculate the Price-to-Earnings (P/E) ratio for a stock based on its dividend.

    Args:
        symbol (str): The stock symbol.
        price (float): The market price of the stock.

    Returns:
        dict: A dictionary containing the P/E ratio (e.g., {"pe_ratio": float}).

    Raises:
        StockNotFoundError: If the symbol does not exist.
    """
    stock = stocks.get(symbol.upper())
    if not stock:
        raise StockNotFoundError(symbol)
    dividend = stock['last_dividend']
    return {"pe_ratio": price / dividend if dividend > 0 else float('inf')}

async def record_trade(trade: Trade) -> dict:
    """
    Record a trade for a specific stock.

    The trade is appended to an in-memory store (deque) grouped by stock symbol.

    Args:
        trade (Trade): A Trade object containing symbol, quantity, price, and trade type.

    Returns:
        dict: A confirmation message (e.g., {"message": "Trade recorded successfully"}).

    Raises:
        StockNotFoundError: If the trade's stock symbol does not exist.
    """
    symbol = trade.symbol.upper()
    if symbol not in stocks:
        raise StockNotFoundError(symbol)

    #below check implemented at first but since I converted the trade_type to Enum, no longer need to manually validate
    # if trade.trade_type not in TradeType.__members__:
    #     raise InvalidTradeTypeError(trade.trade_type)

    trade_entry = {
        "timestamp": datetime.now(),
        "symbol": symbol,
        "quantity": trade.quantity,
        "trade_type": trade.trade_type,
        "price": trade.price,
    }

    trades_by_symbol[symbol].append(trade_entry)

    logger.info(f"[{symbol}] Trade count: {len(trades_by_symbol[symbol])}")

    return {"message": "Trade recorded successfully"}

async def volume_weighted_stock_price(symbol: str, time_window: int = 15) -> dict:
    """
    Calculate the Volume Weighted Stock Price (VWSP) for a stock over a given time window (in minutes).
    
    Args:
        symbol (str): Stock symbol.
        minutes (int): Time window in minutes (default is 15).
    
    Returns:
        dict: {"vwsp": float}
    """

    symbol = symbol.upper()
    if symbol not in stocks:
        raise StockNotFoundError(symbol)
    
    cutoff_time = datetime.now() - timedelta(minutes=time_window)

    trades = trades_by_symbol.get(symbol, deque())
    logger.info(f"[{symbol}] VWSP | Time window: {time_window} minutes | Trade count: {len(trades)}")

    total_price_quantity = 0
    total_quantity = 0

    # Iterate in reverse (most recent first), stop once trades are too old
    for trade in reversed(trades):
        if trade["timestamp"] < cutoff_time:
            break
        total_price_quantity += trade["price"] * trade["quantity"]
        total_quantity += trade["quantity"]


    vwsp = total_price_quantity / total_quantity if total_quantity > 0 else 0
    logger.info(f"[{symbol}] VWSP: {vwsp}")

    return {"vwsp": vwsp}

async def calculate_gbce_index() -> dict:
    """
    Calculate the GBCE All Share Index as the geometric mean of all non-zero VWSPs.
    Uses the same time window as the VWSP function.

    Returns:
    dict: {"gbce_index": float}
    """
    prices = []
    minutes = 15 # hard coded for now, it should go to config
    for symbol in stocks.keys():
        result = await volume_weighted_stock_price(symbol, minutes)
        vwsp = result["vwsp"]
        if vwsp > 0:
            prices.append(vwsp)

    if not prices:
        return {"gbce_index": 0}

    product = 1
    for price in prices:
        product *= price
    
    n = len(prices)
    gbce_index = product ** (1 / n)

    #logger.info(f"Test: square root of 25 :  {25 ** (1/2)}")

    return {"gbce_index": gbce_index}
