from django.urls import path
from . import views

app_name = 'tutoriel'

urlpatterns = [
    path('', views.catalogue, name='catalogue'),
    path('lecon/<int:lecon_id>/', views.lecon_detail, name='lecon_detail'),
    path('quiz/<int:quiz_id>/', views.passer_quiz, name='passer_quiz'),
]