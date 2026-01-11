from django.urls import path
from . import views

app_name = 'avatar'

urlpatterns = [
    path('generate/', views.generate_avatar, name='generate_avatar'),
]