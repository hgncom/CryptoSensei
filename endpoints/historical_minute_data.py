from fastapi import APIRouter, HTTPException
from ..api_requests import get_data_from_api, validate_api_response

router = APIRouter()

@router.get("/get_historical_minute_data/{crypto_name}")
def get_historical_minute_data(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/v2/histominute?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except InvalidCryptoSymbol:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
