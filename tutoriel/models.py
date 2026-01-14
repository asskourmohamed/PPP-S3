from django.db import models
from django.conf import settings
from django.utils import timezone
class Tutorial(models.Model):
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_couverture = models.ImageField(upload_to='tutoriels/couvertures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.titre} (Niveau {self.niveau})"

class Lecon(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='lecons')
    titre = models.CharField(max_length=200)
    ordre = models.IntegerField(default=1)
    video = models.FileField(upload_to='tutoriels/videos/')
    texte_explicatif = models.TextField()
    duree = models.IntegerField(help_text="Durée en secondes")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return f"{self.titre} - {self.tutorial.titre}"

class Quiz(models.Model):
    lecon = models.OneToOneField(Lecon, on_delete=models.CASCADE, related_name='quiz')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pass_mark = models.IntegerField(default=70, help_text="Score minimum pour réussir (%)")
    
    def __str__(self):
        return f"Quiz: {self.titre}"

class Question(models.Model):
    TYPE_CHOICES = [
        ('CHOIX_MULTIPLE', 'Choix multiple'),
        ('VRAI_FAUX', 'Vrai ou Faux'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    type_question = models.CharField(max_length=20, choices=TYPE_CHOICES, default='CHOIX_MULTIPLE')
    ordre = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return f"Q{self.ordre}: {self.question_text[:50]}..."

class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    reponse_text = models.CharField(max_length=500)
    est_correcte = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.reponse_text[:50]}... ({'✓' if self.est_correcte else '✗'})"

# Modèle pour suivre la progression de l'utilisateur
class ProgressionUtilisateur(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progression')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE)
    est_completee = models.BooleanField(default=False)
    date_completion = models.DateTimeField(null=True, blank=True)
    score_quiz = models.IntegerField(null=True, blank=True, help_text="Score du quiz associé (%)")
    temps_passe = models.IntegerField(default=0, help_text="Temps passé en secondes")
    
    class Meta:
        unique_together = ['utilisateur', 'lecon']
        verbose_name_plural = "Progressions Utilisateurs"
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.lecon.titre}"