from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'compte'

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='login'),  # ✅ Doit pointer vers views.connexion
    path('logout/', auth_views.LogoutView.as_view(
        next_page='accueil'
    ), name='logout'),
    path('profil/', views.profil, name='profil'),
]