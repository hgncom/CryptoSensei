from fastapi import APIRouter, HTTPException
from ..api_requests import get_data_from_api, validate_api_response


router = APIRouter()

@router.get("/get_top_cryptos/")
def get_top_cryptos():
    url = f"https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
