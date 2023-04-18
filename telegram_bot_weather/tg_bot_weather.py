import datetime
import requests
import re
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("🏙 Привет! Для того чтобы узнать погоду, нужного тебе города - укажи его координаты."
                        " Долгота-ширина, в формате(XX.XX,XX.XX):")


@dp.message_handler()
async def get_weather(message: types.Message):


    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        location = message.text
        pattern = r"(\d+\.\d+),(\d+\.\d+)"
        match = re.search(pattern, location)
        latitude, longitude = match.groups()
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        cloud = data["clouds"]["all"]
        print(data)


        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nВетер: {wind} м/с\nОблачность: {cloud}\n"
              f"***Хорошего дня!***"
              )

    except:
        await message.reply("\U00002620 Проверьте координаты \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)