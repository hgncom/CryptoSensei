from fastapi import APIRouter
from api_requests import get_data_from_api, ExternalAPIError, InvalidCryptoSymbol
from config import BINANCE_API_BASE_URL

router = APIRouter()

def make_binance_request(route: str, params: dict = {}):
    url = f"{BINANCE_API_BASE_URL}/api/v3/{route}"
    try:
        return get_data_from_api(url, params=params)
    except ExternalAPIError as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)

@router.get("/get_binance_price/{crypto_name}")
def get_crypto_price(crypto_name: str):
    params = {'symbol': f"{crypto_name}USDT"}
    return make_binance_request('ticker/price', params)

@router.get("/get_binance_historical/{crypto_name}/{interval}")
def get_binance_historical(crypto_name: str, interval: str):
    params = {'symbol': f"{crypto_name}USDT", 'interval': interval}
    return make_binance_request('klines', params)

@router.get("/get_binance_orderbook/{crypto_name}")
def get_binance_orderbook(crypto_name: str):
    params = {'symbol': f"{crypto_name}USDT"}
    return make_binance_request('depth', params)

@router.get("/get_binance_trades/{crypto_name}")
def get_binance_trades(crypto_name: str):
    params = {'symbol': f"{crypto_name}USDT"}
    return make_binance_request('trades', params)
