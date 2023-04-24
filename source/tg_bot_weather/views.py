import json

import telebot
import requests
import re
from main.settings import OPEN_WEATHER_TOKEN, TG_BOT_TOKEN
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


bot = telebot.TeleBot(TG_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🏙 Привет! Для того чтобы узнать погоду, нужного тебе города - укажи его координаты. Долгота-ширина, в формате(XX.XX,XX.XX):")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
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

        bot.send_message(
            message.chat.id,
            text=f"Погода в городе: {city}\nТемпература: {cur_weather}C°\nВлажность: {humidity}%\nВетер: {wind} м/с\nОблачность: {cloud}\n"
        )
    except:
        bot.send_message(
            message.chat.id,
            text="Проверьте координаты"
        )


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        try:
            json_data = json.loads(json_str)
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            return HttpResponseBadRequest()

        print(json_data)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return HttpResponse('')
    else:
        return HttpResponse('Hello from Django!')