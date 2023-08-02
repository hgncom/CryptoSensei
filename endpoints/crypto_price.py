from fastapi import APIRouter, HTTPException
import json
from CryptoSensei.api_requests import get_data_from_api, validate_api_response

router = APIRouter()

@router.get("/get_crypto_price/{crypto_name}")  # This makes the function an HTTP endpoint
def get_crypto_price(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/price?fsym={crypto_name}&tsyms=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
