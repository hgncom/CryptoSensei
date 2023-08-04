from cachetools import TTLCache
from config import CRYPTOCOMPARE_API_BASE_URL, CRYPTOCOMPARE_API_KEY
from fastapi import HTTPException
from json import JSONDecodeError
from requests.exceptions import RequestException
import requests

# Create a cache with a time-to-live (TTL) of 600 seconds (10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

# Custom Exception classes with detailed messages
class ExternalAPIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=detail)

class APIResponseError(HTTPException):
    def __init__(self, message: str = "Error in API response."):
        super().__init__(status_code=502, detail=message)

class JSONDecodeError(HTTPException):
    def __init__(self, message: str = "Error decoding data from the external API."):
        super().__init__(status_code=502, detail=message)

class InvalidCryptoSymbol(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="The requested cryptocurrency symbol was not found.")


# Validate API response format
def validate_api_response(response):
    if response.status_code != 200:
        detail = f"Received a non-200 response from the external API: {response.status_code}"
        raise ExternalAPIError(detail=detail)

    try:
        data = response.json()
        return data
    except JSONDecodeError as e:
        detail = f"Error decoding data from the external API: {str(e)}"
        raise ExternalAPIError(detail=detail)

# Initializing the cache
cache = {}

def get_data_from_api(url, params={}, auth_required=False):
    headers = {}

    # If authorization is required, set the header
    if auth_required:
        headers = {
            "Authorization": f"Apikey {CRYPTOCOMPARE_API_KEY}"
        }

    # Chec  k if the response is already cached
    if url in cache:
        return cache[url]
    else:
        # If not cached, make the API call and cache the response
        try:
            response = requests.get(url, headers=headers, params=params)
            data = validate_api_response(response)
            cache[url] = data
            return data
        except RequestException as e:
            if e.response is not None:
                # If the error has an associated HTTP response, provide its details
                detail = f"An error occurred while fetching data from the external API: {e.response.text}"
            else:
                # Otherwise, just provide the error message
                detail = str(e)
            raise ExternalAPIError(detail=detail)