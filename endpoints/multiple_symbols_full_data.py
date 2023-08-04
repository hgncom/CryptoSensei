from fastapi import APIRouter
from api_requests import ExternalAPIError
from api import crypto_service

router = APIRouter()

@router.get("/get_multiple_symbols_full_data/{crypto_names}/{currency_names}")
def get_multiple_symbols_full_data(crypto_names: str, currency_names: str):
    try:
        data = crypto_service.get_multiple_symbols_full_data(crypto_names, currency_names)
        return data
    except ExternalAPIError as e:
        raise e
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)