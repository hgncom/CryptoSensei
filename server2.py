import sys
import os

# Get the absolute path of the "CryptoSensei" directory
crypto_sensei_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the parent directory (the root folder of the project)
project_root = os.path.dirname(crypto_sensei_dir)

# Append the project root to the Python path
sys.path.append(project_root)


from fastapi import FastAPI, HTTPException, Depends
from api_requests import get_data_from_api, validate_api_response
from endpoints import (
    ai_plugin,
    crypto_price,
    historical_daily_data,
    historical_hourly_data,
    historical_minute_data,
    crypto_news,
    top_cryptos,
    social_media_stats,
    average_price,
)

app = FastAPI()

# Include all the router modules with their dependencies
app.include_router(ai_plugin.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(crypto_price.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(historical_daily_data.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(historical_hourly_data.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(historical_minute_data.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(crypto_news.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(top_cryptos.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(social_media_stats.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
app.include_router(average_price.router, dependencies=[Depends(get_data_from_api), Depends(validate_api_response)])
