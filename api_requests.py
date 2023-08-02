from fastapi import HTTPException
import requests
from cachetools import TTLCache
import json

# Constants for API URLs
CRYPTOCOMPARE_API_BASE_URL = "https://min-api.cryptocompare.com/data"

# Create a cache with a time-to-live (TTL) of 600 seconds (10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

# Custom Exception class with detailed message
class ExternalAPIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=detail)

# Validate API response format
def validate_api_response(response):
    if response.status_code != 200:
        raise ExternalAPIError(detail="An error occurred while fetching data from the external API.")

    try:
        data = response.json()
        return data
    except json.JSONDecodeError:
        raise ExternalAPIError(detail="Error decoding data from the external API.")

def get_data_from_api(url):
    # Check if the response is already cached
    if url in cache:
        return cache[url]
    else:
        # If not cached, make the API call and cache the response
        try:
            response = requests.get(url)
            data = validate_api_response(response)
            cache[url] = data
            return data
        except requests.exceptions.RequestException:
            raise ExternalAPIError(detail="An error occurred while fetching data from the external API.")
