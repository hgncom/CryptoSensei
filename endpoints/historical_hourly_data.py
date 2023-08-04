from fastapi import APIRouter
from api_requests import ExternalAPIError
from api import crypto_service

router = APIRouter()

@router.get("/get_historical_hourly_data/{crypto_name}")
def get_historical_hourly_data(crypto_name: str):
    try:
        data = crypto_service.get_historical_daily_data(crypto_name)
        return data
    except ExternalAPIError as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)
