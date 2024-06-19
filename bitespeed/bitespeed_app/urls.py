
from django.urls import path

from bitespeed_app import views


urlpatterns = [
   path('', views.post_identity, name='post_data')
]