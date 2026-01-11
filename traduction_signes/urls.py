from django.urls import path
from . import views

app_name = 'traduction'

urlpatterns = [
    path('signe-texte/', views.signe_vers_texte, name='signe_vers_texte'),
    path('texte-signe/', views.texte_vers_signe, name='texte_vers_signe'),
]