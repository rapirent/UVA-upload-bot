from django.conf.urls import include, url
from telegram_bot import views

urlpatterns = [
    url(r'^hook/$', views.webhook, name='webhook'),
    url(r'^state/', views.showState, name='state'),
]
