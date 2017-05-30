from django.conf.urls import include, url
from telegram_bot import views

urlpatterns = [
    url(r'^state/', views.showState, name='state'),
]
