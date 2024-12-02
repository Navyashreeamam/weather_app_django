from django.urls import path
from .import weatherEngine

urlpatterns = [
    path('', weatherEngine.index),
]