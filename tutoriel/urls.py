from django.urls import path
from . import views

app_name = 'tutoriel'

urlpatterns = [
    # Catalogue
    path('', views.catalogue_tutoriels, name='catalogue'),
    
    # Tutoriels et leçons
    path('tutorial/<int:tutorial_id>/', views.catalogue_tutoriels, name='tutorial_detail'),
    path('tutorial/<int:tutorial_id>/lecon/<int:lecon_id>/', 
         views.lecon_detail, name='lecon_detail'),
    
    # Quiz
    path('quiz/<int:quiz_id>/', views.passer_quiz, name='passer_quiz'),
    path('quiz/<int:quiz_id>/resultat/', views.passer_quiz, name='quiz_resultat'),
    
    # Progression
    path('progression/', views.ma_progression, name='progression'),
    path('progression/<int:tutorial_id>/', views.ma_progression, name='progression_tutorial'),
    
    # API (optionnel pour plus tard)
    # path('api/complete-lecon/', views.complete_lecon, name='complete_lecon'),
]