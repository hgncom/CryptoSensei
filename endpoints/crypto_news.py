from fastapi import HTTPException, APIRouter
import json
from ..api_requests import get_data_from_api, validate_api_response

router = APIRouter()

@router.get("/get_crypto_news")
def get_crypto_news():
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/v2/news/?lang=EN"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
