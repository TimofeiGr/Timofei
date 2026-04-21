import os
import aiohttp
from dotenv import load_dotenv
from typing import Union  

load_dotenv()
API_KEY = "24ffbb92d03795668d7483e91517f7c6"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(city: str = None, lat: float = None, lon: float = None) -> Union[str, dict]:

    if not API_KEY:
        return "❌ Ошибка: не указан API ключ в .env файле."

    params = {"appid": API_KEY, "units": "metric", "lang": "ru"}
    if city:
        params["q"] = city
    elif lat and lon:
        params["lat"] = lat
        params["lon"] = lon
    else:
        return "❌ Укажите город или отправьте геолокацию."

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, params=params, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return "🌍 Город не найден. Проверьте название (например: Moscow)."
                elif response.status == 401:
                    return "🔑 Ошибка авторизации. Проверьте API-ключ."
                else:
                    return f"⚠️ Ошибка сервера погоды: {response.status}"
    except aiohttp.ClientError as e:
        return f"🌐 Сетевая ошибка: {e}"
    except Exception as e:
        return f"❌ Неизвестная ошибка: {e}
