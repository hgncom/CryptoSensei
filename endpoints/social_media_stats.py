from fastapi import APIRouter
from api_requests import ExternalAPIError, InvalidCryptoSymbol
from api import crypto_service

router = APIRouter()

@router.get("/get_social_media_stats/{crypto_name}")
def get_social_media_stats(crypto_name: str):
    try:
        data = crypto_service.get_social_media_stats(crypto_name)
        return data
    except (ExternalAPIError, InvalidCryptoSymbol) as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)
