from fastapi import FastAPI, HTTPException
import requests
from cachetools import TTLCache

app = FastAPI()

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '54df13ccb6d85f51b60c3640192b834f8d7cd28a8c96948f71062d08030d6806'

# Create a cache with a time-to-live (TTL) of 300 seconds (5 minutes)
cache = TTLCache(maxsize=100, ttl=300)

def get_data_from_api(url):
    # Check if the response is already cached
    if url in cache:
        return cache[url]
    else:
        # If not cached, make the API call and cache the response
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cache[url] = data
            return data
        else:
            raise HTTPException(status_code=500, detail="An error occurred while fetching data from the external API.")

@app.get("/get_crypto_price/{crypto_name}")
def get_crypto_price(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_name}&tsyms=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_historical_daily_data/{crypto_name}")
def get_historical_daily_data(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_historical_hourly_data/{crypto_name}")
def get_historical_hourly_data(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_historical_minute_data/{crypto_name}")
def get_historical_minute_data(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/v2/histominute?fsym={crypto_name}&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_crypto_news")
def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_top_cryptos/")
def get_top_cryptos():
    url = "https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USD"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_social_media_stats/{crypto_name}")
def get_social_media_stats(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/all/coinlist"
    try:
        response = requests.get(url)
        coin_list = response.json()
        if crypto_name not in coin_list['Data']:
            raise HTTPException(status_code=400, detail="Invalid cryptocurrency symbol")

        coin_id = coin_list['Data'][crypto_name]['Id']
        url = f"https://min-api.cryptocompare.com/data/social/coin/latest?coinId={coin_id}&api_key={api_key}"
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

@app.get("/get_average_price/{crypto_name}")
def get_average_price(crypto_name: str):
    url = f"https://min-api.cryptocompare.com/data/generateAvg?fsym={crypto_name}&tsym=USD&e=Kraken"
    try:
        data = get_data_from_api(url)
        return data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)  # Ensure it's listening on port 8080
