from fastapi import APIRouter
from api_requests import ExternalAPIError, InvalidCryptoSymbol
from api import cryptocompare

router = APIRouter()

@router.get(
    "/get_average_price/{crypto_name}",
    summary="Average price",
    description="This endpoint returns the average price of a specified cryptocurrency over a certain period. The data is retrieved from the CryptoCompare API, specifically from the 'generateAvg' endpoint. The average price is calculated based on the provided cryptocurrency symbol (e.g., 'BTC' for Bitcoin) and it is returned in USD."
)
def get_average_price(crypto_name: str):
    try:
        # Call the function from the cryptocompare module here
        data = crypto_service.get_average_price(crypto_name)
        return data
    except ExternalAPIError as e:
        raise e
    except InvalidCryptoSymbol as e:
        detail = f"Invalid cryptocurrency symbol: {str(e)}"
        raise ExternalAPIError(status_code=400, detail=detail)
    except Exception as e:
        detail = f"An unexpected error occurred while processing the request: {str(e)}"
        raise ExternalAPIError(detail=detail)

