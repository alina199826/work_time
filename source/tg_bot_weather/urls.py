from django.urls import path
from tg_bot_weather.views import telegram_webhook

urlpatterns = [
    path('setWebhook/', telegram_webhook),
]