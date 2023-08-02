from fastapi import APIRouter

router = APIRouter()

# Import all your router modules here
from CryptoSensei.endpoints import ai_plugin, crypto_price, historical_daily_data, historical_hourly_data, historical_minute_data, crypto_news, top_cryptos, social_media_stats, average_price

# Include all the router modules
router.include_router(ai_plugin.router)
router.include_router(crypto_price.router)
router.include_router(historical_daily_data.router)
router.include_router(historical_hourly_data.router)
router.include_router(historical_minute_data.router)
router.include_router(crypto_news.router)
router.include_router(top_cryptos.router)
router.include_router(social_media_stats.router)
router.include_router(average_price.router)