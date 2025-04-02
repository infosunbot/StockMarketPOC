import pytest
from app.services import stock_service
from app.models.trade import Trade
from app.data import stocks_data
from datetime import datetime, timedelta


def setup_function():
    # Clear trades before each test
    stocks_data.trades_by_symbol.clear()

@pytest.mark.asyncio
async def test_calculate_dividend_yield_common():
    result = await stock_service.calculate_dividend_yield("POP", 100)
    assert result["dividend_yield"] == 0.08

@pytest.mark.asyncio
async def test_calculate_dividend_yield_preferred():
    result = await stock_service.calculate_dividend_yield("GIN", 100)
    assert result["dividend_yield"] == 0.02

@pytest.mark.asyncio
async def test_calculate_pe_ratio_valid():
    result = await stock_service.calculate_pe_ratio("ALE", 230)
    assert result["pe_ratio"] == 10.0

@pytest.mark.asyncio
async def test_calculate_pe_ratio_zero_dividend():
    result = await stock_service.calculate_pe_ratio("TEA", 100)
    assert result["pe_ratio"] == float("inf")

@pytest.mark.asyncio
async def test_record_trade():
    trade = Trade(symbol="POP", quantity=50, trade_type="buy", price=120.0)
    response = await stock_service.record_trade(trade)
    assert response["message"] == "Trade recorded successfully"
    assert len(stocks_data.trades_by_symbol["POP"]) == 1

@pytest.mark.asyncio
async def test_volume_weighted_stock_price():
    # Add trades
    now = datetime.now()
    stocks_data.trades_by_symbol["JOE"].append({"symbol": "JOE", "quantity": 30, "price": 200, "trade_type": "buy", "timestamp": now})
    stocks_data.trades_by_symbol["JOE"].append({"symbol": "JOE", "quantity": 70, "price": 300, "trade_type": "sell", "timestamp": now})
    result = await stock_service.volume_weighted_stock_price("JOE")
    assert result["vwsp"] == pytest.approx(270.0)

@pytest.mark.asyncio
async def test_volume_weighted_stock_price_no_trades():
    result = await stock_service.volume_weighted_stock_price("GIN")
    assert result["vwsp"] == 0

@pytest.mark.asyncio
async def test_calculate_gbce_index():
    now = datetime.now()
    stocks_data.trades_by_symbol["TEA"].append({"symbol": "TEA", "quantity": 20, "price": 100, "trade_type": "buy", "timestamp": now})
    stocks_data.trades_by_symbol["POP"].append({"symbol": "POP", "quantity": 40, "price": 200, "trade_type": "sell", "timestamp": now})
    result = await stock_service.calculate_gbce_index()
    assert result["gbce_index"] > 0
