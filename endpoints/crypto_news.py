from fastapi import APIRouter
from api_requests import ExternalAPIError
from api import crypto_service

router = APIRouter()

@router.get("/get_crypto_news")
def get_crypto_news():
    try:
        data = crypto_service.get_crypto_news()
        return data
    except ExternalAPIError as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)

