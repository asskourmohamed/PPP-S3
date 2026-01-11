
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def catalogue(request):
    """Catalogue des tutoriels"""
    return render(request, 'tutoriel/catalogue.html')

@login_required
def lecon_detail(request, lecon_id):
    """Détail d'une leçon"""
    return render(request, 'tutoriel/lecon_detail.html', {'lecon_id': lecon_id})

@login_required
def passer_quiz(request, quiz_id):
    """Page pour passer un quiz"""
    return render(request, 'tutoriel/quiz.html', {'quiz_id': quiz_id})