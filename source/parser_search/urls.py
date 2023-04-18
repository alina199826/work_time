from django.urls import path
from parser_search import views_parser

urlpatterns = [
    path('', views_parser.search, name='search'),
]