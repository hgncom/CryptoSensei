from fastapi import APIRouter, HTTPException
from ..api_requests import get_data_from_api, validate_api_response


router = APIRouter()

@router.get("/get_historical_hourly_data/{crypto_name}")
def get_historical_hourly_data(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
