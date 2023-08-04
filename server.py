import sys
import os
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api_requests import get_data_from_api, validate_api_response
from endpoints import (
    crypto_price,
    historical_daily_data,
    historical_hourly_data,
    historical_minute_data,
    crypto_news,
    top_cryptos,
    social_media_stats,
    average_price,
    multiple_symbols_full_data,   # Add this line
)

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Append the project root to the Python path
sys.path.append(project_root)

app = FastAPI()

# Set up the Templates object
templates = Jinja2Templates(directory=os.path.join(project_root, "templates"))

# Mount static files
static_dir = os.path.join(project_root, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Main page with plugin documentation
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url='/docs')

# Include all the router modules with their dependencies
app.include_router(crypto_price.router)
app.include_router(historical_daily_data.router)
app.include_router(historical_hourly_data.router)
app.include_router(historical_minute_data.router)
app.include_router(crypto_news.router)
app.include_router(top_cryptos.router)
app.include_router(social_media_stats.router)
app.include_router(average_price.router)
app.include_router(multiple_symbols_full_data.router)   # Add this line
