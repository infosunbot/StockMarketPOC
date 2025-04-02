from fastapi import APIRouter, HTTPException
from app.models.trade import Trade
from app.services.stock_service import (
    calculate_dividend_yield,
    calculate_pe_ratio,
    record_trade,
    volume_weighted_stock_price,
    calculate_gbce_index,
)
from app.exceptions import StockNotFoundError, InvalidTradeTypeError

router = APIRouter()


@router.get("/stocks/{symbol}/dividend-yield")
async def get_dividend_yield(symbol: str, price: float):
    try:
        return await calculate_dividend_yield(symbol, price)
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/stocks/{symbol}/pe-ratio")
async def get_pe_ratio(symbol: str, price: float):
    try:
        return await calculate_pe_ratio(symbol, price)
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/trades")
async def post_trade(trade: Trade):
    try:
        return await record_trade(trade)
    except (StockNotFoundError, InvalidTradeTypeError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stocks/{symbol}/vwsp")
async def get_vwsp(symbol: str):
    try:
        return await volume_weighted_stock_price(symbol)
    except StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/market/gbce")
async def get_index():
    return await calculate_gbce_index()
