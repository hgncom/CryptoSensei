from fastapi import APIRouter, HTTPException
from ..api_requests import get_data_from_api, validate_api_response


router = APIRouter()

@router.get("/get_social_media_stats/{crypto_name}")
def get_social_media_stats(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/all/coinlist"
    try:
        response = get_data_from_api(url)
        coin_list = response["Data"]

        if crypto_name not in coin_list:
            raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")

        coin_id = coin_list[crypto_name]["Id"]
        social_url = f"https://min-api.cryptocompare.com/data/social/coin/latest?coinId={coin_id}"
        data = get_data_from_api(social_url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
