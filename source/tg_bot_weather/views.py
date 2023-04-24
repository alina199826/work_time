from datetime import datetime
import telebot
import requests
import re

TG_BOT_TOKEN = '6083711043:AAFKndqfOzGq3PYHE57ZWRZ59yqehSczl6k'
OPEN_WEATHER_TOKEN = 'ad5236a5c0c86db0a0f1263cc15bc76f'

bot = telebot.TeleBot(TG_BOT_TOKEN)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id,
             "🏙 Привет! Для того чтобы узнать погоду, нужного тебе города - укажи его координаты."
             " Долгота-ширина, в формате(XX.XX,XX.XX):")


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
    print(data)

    bot.send_message(
      message.chat.id,
      text=f"***{datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
         f"Погода в городе: {city}\nТемпература: {cur_weather}C° \n"
         f"Влажность: {humidity}%\nВетер: {wind} м/с\nОблачность: {cloud}\n"
         f"***Хорошего дня!***"
    )
  except:
    bot.send_message(
      message.chat.id,
      text="\U00002620 Проверьте координаты \U00002620"
    )



bot.infinity_polling()