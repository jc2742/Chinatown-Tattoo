from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('info', index),
    path('login', index)
]
