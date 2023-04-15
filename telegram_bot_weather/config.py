from decouple import config

open_weather_token = config('open_weather_token', default='')
tg_bot_token = config('tg_bot_token', default='')