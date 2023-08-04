from fastapi import APIRouter
from api_requests import ExternalAPIError
from api import crypto_service

router = APIRouter()

@router.get("/get_crypto_price/{crypto_name}")  # This makes the function an HTTP endpoint
def get_crypto_price(crypto_name: str):
    try:
        data = crypto_service.get_crypto_price(crypto_name)
        return data
    except ExternalAPIError as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)

