from fastapi import FastAPI
from app.api.routes import router as stock_router
import logging

app = FastAPI(title="Stock Market API")
app.include_router(stock_router)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)