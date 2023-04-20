
from datetime import datetime
from tg_bot_weather.bot_settings import OPEN_WEATHER_TOKEN, TG_BOT_TOKEN
import requests
import re
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from asgiref.sync import async_to_sync

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("🏙 Привет! Для того чтобы узнать погоду, нужного тебе города - укажи его координаты."
                        " Долгота-ширина, в формате(XX.XX,XX.XX):")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        location = message.text
        pattern = r"(\d+\.\d+),(\d+\.\d+)"
        match = re.search(pattern, location)
        latitude, longitude = match.groups()
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_TOKEN}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]


        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        cloud = data["clouds"]["all"]
        print(data)

        await bot.send_message(
            chat_id=message.chat.id,
            text=f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                 f"Погода в городе: {city}\nТемпература: {cur_weather}C° \n"
                 f"Влажность: {humidity}%\nВетер: {wind} м/с\nОблачность: {cloud}\n"
                 f"***Хорошего дня!***"
        )
    except:
        await bot.send_message(
            chat_id=message.chat.id,
            text="\U00002620 Проверьте координаты \U00002620"
        )


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        update = types.Update(**request.POST.dict())
        async_to_sync(dp.process_update)(update)
        return HttpResponse(status=200)
    elif request.method == 'GET':
        return HttpResponse('This is a Telegram bot webhook URL.')
    else:
        return HttpResponse(status=405)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
