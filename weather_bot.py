import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from weather_api import fetch_weather

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот погоды.\n"
        "Отправьте /weather <город> или вашу геолокацию, "
        "чтобы узнать текущую погоду."
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 Команды:\n"
        "🔹 /start — приветствие\n"
        "🔹 /weather <город> — погода в городе\n"
        "🔹 📍 Отправьте точку на карте — погода по координатам"
    )

@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("📝 Пример использования: `/weather Москва`", parse_mode="Markdown")
        return
    
    city = args[1]
    await _send_weather(message, city=city)

@dp.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await _send_weather(message, lat=lat, lon=lon)

async def _send_weather(message: Message, city=None, lat=None, lon=None):
    """Вспомогательная функция для получения и форматирования погоды"""
    status_msg = await message.answer("⏳ Загружаю данные...")
    
    data = await fetch_weather(city=city, lat=lat, lon=lon)
    
    if isinstance(data, str):  # Если пришла ошибка (строка)
        await status_msg.edit_text(data)
        return

    # Парсинг JSON-ответа
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    city_name = data["name"]

    text = (
        f"🌤 Погода в **{city_name}**\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"☁️ Описание: {desc.capitalize()}\n"
        f"💧 Влажность: {humidity}%\n"
        f"💨 Ветер: {wind} м/с"
    )
    await status_msg.edit_text(text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())