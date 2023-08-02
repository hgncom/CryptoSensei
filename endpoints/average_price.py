from fastapi import HTTPException, APIRouter
from ..api_requests import get_data_from_api, validate_api_response

router = APIRouter()

@router.get("/get_average_price/{crypto_name}")
def get_average_price(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/generateAvg?fsym={crypto_name}&tsym=USD&e=Kraken"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")