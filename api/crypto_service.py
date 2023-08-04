from api import cryptocompare, binance
from api_requests import ExternalAPIError, InvalidCryptoSymbol

def get_average_price(symbol: str):
    try:
        return cryptocompare.get_average_price(symbol)
    except ExternalAPIError:
        return binance.get_average_price(symbol)

def get_crypto_news():
    try:
        return cryptocompare.get_crypto_news()
    except ExternalAPIError:
        # Note: Here you need to ensure binance has the similar endpoint
        return binance.get_crypto_news()

def get_crypto_price(symbol: str):
    try:
        return cryptocompare.get_crypto_price(symbol)
    except ExternalAPIError:
        return binance.get_crypto_price(symbol)

def get_historical_daily_data(symbol: str):
    try:
        return cryptocompare.get_historical_daily_data(symbol)
    except ExternalAPIError:
        return binance.get_historical_daily_data(symbol)

def get_historical_hourly_data(symbol: str):
    try:
        return cryptocompare.get_historical_hourly_data(symbol)
    except ExternalAPIError:
        return binance.get_historical_hourly_data(symbol)

def get_historical_minute_data(symbol: str):
    try:
        return cryptocompare.get_historical_minute_data(symbol)
    except InvalidCryptoSymbol as e:
        raise e
    except ExternalAPIError:
        return binance.get_historical_minute_data(symbol)

def get_social_media_stats(symbol: str):
    try:
        return cryptocompare.get_social_media_stats(symbol)
    except (ExternalAPIError, InvalidCryptoSymbol) as e:
        raise e
    # Note: Here you need to ensure binance has the similar endpoint
    except Exception:
        return binance.get_social_media_stats(symbol)

def get_top_cryptos():
    try:
        return cryptocompare.get_top_cryptos()
    except ExternalAPIError:
        # Note: Here you need to ensure binance has the similar endpoint
        return binance.get_top_cryptos()

def get_multiple_symbols_full_data(crypto_names: str, currency_names: str):
    try:
        return cryptocompare.get_multiple_symbols_full_data(crypto_names, currency_names)
    except ExternalAPIError:
        # Note: Binance does not seem to provide a similar endpoint for multi symbol full data
        raise
