from fastapi import APIRouter
from api_requests import get_data_from_api, ExternalAPIError, InvalidCryptoSymbol
from config import CRYPTOCOMPARE_API_BASE_URL

router = APIRouter()

def make_cryptocompare_request(route: str, params: dict = {}, auth_required: bool = False):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/{route}"
    try:
        return get_data_from_api(url, params, auth_required)
    except ExternalAPIError as e:
        raise e
    except InvalidCryptoSymbol as e:
        detail = f"Invalid cryptocurrency symbol: {str(e)}"
        raise ExternalAPIError(detail=detail)
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)

@router.get("/get_average_price/{crypto_name}")
def get_average_price(crypto_name: str):
    params = {'fsym': crypto_name, 'tsym': 'USD', 'e': 'Kraken'}
    return make_cryptocompare_request('generateAvg', params)

@router.get("/get_crypto_news")
def get_crypto_news():
    return make_cryptocompare_request('v2/news/?lang=EN')

@router.get("/get_crypto_price/{crypto_name}")
def get_crypto_price(crypto_name: str):
    params = {'fsym': crypto_name, 'tsyms': 'USD'}
    return make_cryptocompare_request('price', params)

@router.get("/get_historical_daily_data/{crypto_name}")
def get_historical_daily_data(crypto_name: str):
    params = {'fsym': crypto_name, 'tsym': 'USD'}
    return make_cryptocompare_request('v2/histoday', params)

@router.get("/get_historical_hourly_data/{crypto_name}")
def get_historical_hourly_data(crypto_name: str):
    params = {'fsym': crypto_name, 'tsym': 'USD'}
    return make_cryptocompare_request('v2/histohour', params)

@router.get("/get_historical_minute_data/{crypto_name}")
def get_historical_minute_data(crypto_name: str):
    params = {'fsym': crypto_name, 'tsym': 'USD'}
    return make_cryptocompare_request('v2/histominute', params)

@router.get("/get_social_media_stats/{crypto_name}")
def get_social_media_stats(crypto_name: str):
    coin_list = make_cryptocompare_request('all/coinlist', auth_required=True)["Data"]

    if crypto_name not in coin_list:
        detail = f"Invalid cryptocurrency symbol: {crypto_name}"
        raise InvalidCryptoSymbol(detail=detail)

    coin_id = coin_list[crypto_name]["Id"]
    params = {'coinId': coin_id}
    return make_cryptocompare_request('social/coin/latest', params, auth_required=True)

@router.get("/get_top_cryptos/")
def get_top_cryptos():
    params = {'limit': '10', 'tsym': 'USD'}
    return make_cryptocompare_request('top/mktcapfull', params)

@router.get("/get_multiple_symbols_full_data/{crypto_names}/{currency_names}")
def get_multiple_symbols_full_data(crypto_names: str, currency_names: str):
    params = {'fsyms': crypto_names, 'tsyms': currency_names}
    return make_cryptocompare_request('pricemultifull', params)

