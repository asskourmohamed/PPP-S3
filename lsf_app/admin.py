from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    # Champs à afficher dans la liste
    list_display = ('username', 'email', 'type_utilisateur', 'niveau_langue_signes', 'is_staff', 'date_inscription')
    
    # Filtres disponibles
    list_filter = ('type_utilisateur', 'niveau_langue_signes', 'is_staff', 'is_active')
    
    # Champs de recherche
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Groupement des champs dans le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'bio')}),
        ('Profil LSF', {'fields': ('type_utilisateur', 'niveau_langue_signes', 'avatar_personnalise')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined', 'date_inscription')}),
    )
    
    # ⭐⭐ CORRECTION ICI ⭐⭐ - Ajout de 'niveau_langue_signes'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'type_utilisateur', 'niveau_langue_signes', 'password1', 'password2'),
        }),
    )
    
    # Tri par défaut
    ordering = ('-date_inscription',)