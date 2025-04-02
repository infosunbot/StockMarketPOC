from pydantic import BaseModel
from app.models.enums import TradeType

class Trade(BaseModel):
    symbol: str
    quantity: int
    trade_type: TradeType # buy or sell
    price: float
