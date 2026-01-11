from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    TYPE_UTILISATEUR = [
        ('SOURD', 'Sourd'),
        ('APPRENANT', 'Apprenant'),
        ('INTERPRETE', 'Interprète'),
        ('ADMIN', 'Administrateur'),
    ]
    
    type_utilisateur = models.CharField(
        max_length=20, 
        choices=TYPE_UTILISATEUR, 
        default='APPRENANT'
    )
    niveau_langue_signes = models.IntegerField(default=1)
    date_inscription = models.DateTimeField(auto_now_add=True)
    avatar_personnalise = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True
    )
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.type_utilisateur})"
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"