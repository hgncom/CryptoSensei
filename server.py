from fastapi import FastAPI, HTTPException
import requests
from cachetools import TTLCache
import json
import os

app = FastAPI()

# Constants for API URLs
CRYPTOCOMPARE_API_BASE_URL = "https://min-api.cryptocompare.com/data"
CRYPTOCOMPARE_API_KEY = '54df13ccb6d85f51b60c3640192b834f8d7cd28a8c96948f71062d08030d6806'

# Create a cache with a time-to-live (TTL) of 300 seconds (5 minutes)
cache = TTLCache(maxsize=100, ttl=300)

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
        raise ExternalAPIError(detail="An error occurred while fetching data from the external API.")

    try:
        data = response.json()
        if "Response" in data and data["Response"] == "Error":
            raise APIResponseError()
        return data
    except json.JSONDecodeError:
        raise JSONDecodeError()

# Endpoint to serve the ai-plugin.json file as raw JSON
@app.get("/ai-plugin.json")
def ai_plugin():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "ai-plugin.json")

        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="ai-plugin.json not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

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

@app.get("/get_crypto_price/{crypto_name}")
def get_crypto_price(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/price?fsym={crypto_name}&tsyms=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except InvalidCryptoSymbol:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_historical_daily_data/{crypto_name}")
def get_historical_daily_data(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/v2/histoday?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except InvalidCryptoSymbol:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_historical_hourly_data/{crypto_name}")
def get_historical_hourly_data(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/v2/histohour?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except InvalidCryptoSymbol:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_historical_minute_data/{crypto_name}")
def get_historical_minute_data(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/v2/histominute?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except InvalidCryptoSymbol:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_crypto_news")
def get_crypto_news():
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/v2/news/?lang=EN"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_top_cryptos/")
def get_top_cryptos():
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/top/mktcapfull?limit=10&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_social_media_stats/{crypto_name}")
def get_social_media_stats(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/all/coinlist"
    try:
        response = requests.get(url)
        coin_list = validate_api_response(response)

        if crypto_name not in coin_list['Data']:
            raise InvalidCryptoSymbol()

        coin_id = coin_list['Data'][crypto_name]['Id']
        url = f"{CRYPTOCOMPARE_API_BASE_URL}/social/coin/latest?coinId={coin_id}&api_key={CRYPTOCOMPARE_API_KEY}"
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_average_price/{crypto_name}")
def get_average_price(crypto_name: str):
    url = f"{CRYPTOCOMPARE_API_BASE_URL}/generateAvg?fsym={crypto_name}&tsym=USD&e=Kraken"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except InvalidCryptoSymbol:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)  # Ensure it's listening on port 8080
