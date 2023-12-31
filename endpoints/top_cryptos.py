from fastapi import APIRouter
from api_requests import ExternalAPIError
from api import crypto_service

router = APIRouter()

@router.get("/get_top_cryptos/")
def get_top_cryptos():
    try:
        data = crypto_service.get_top_cryptos()
        return data
    except ExternalAPIError as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)
