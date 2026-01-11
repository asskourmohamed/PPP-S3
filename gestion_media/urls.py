from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    path('upload/video/', views.upload_video, name='upload_video'),
]