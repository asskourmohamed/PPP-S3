from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from .models import Tutorial, Lecon, Quiz, Question, ProgressionUtilisateur
from .forms import QuizForm  # Nous créerons ce formulaire après

def catalogue_tutoriels(request):
    """Page d'accueil des tutoriels"""
    tutorials = Tutorial.objects.annotate(
        nombre_lecons=Count('lecons'),
        duree_totale= Sum('lecons__duree')
    )
    
    # Pour les utilisateurs connectés, ajouter la progression
    if request.user.is_authenticated:
        for tutorial in tutorials:
            tutorial.progression = ProgressionUtilisateur.objects.filter(
                utilisateur=request.user,
                tutorial=tutorial,
                est_completee=True
            ).count()
            tutorial.total_lecons = tutorial.lecons.count()
            tutorial.percentage = int((tutorial.progression / tutorial.total_lecons * 100)) if tutorial.total_lecons > 0 else 0
    
    return render(request, 'tutoriel/catalogue.html', {
        'tutorials': tutorials,
        'page_title': 'Catalogue des Tutoriels'
    })

@login_required
def lecon_detail(request, tutorial_id, lecon_id):
    """Détail d'une leçon avec vidéo"""
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    lecon = get_object_or_404(Lecon, id=lecon_id, tutorial=tutorial)
    
    # Récupérer ou créer la progression
    progression, created = ProgressionUtilisateur.objects.get_or_create(
        utilisateur=request.user,
        tutorial=tutorial,
        lecon=lecon,
        defaults={'est_completee': False}
    )
    
    # Récupérer les leçons précédentes/suivantes
    lecons = list(tutorial.lecons.all())
    current_index = lecons.index(lecon)
    prev_lecon = lecons[current_index - 1] if current_index > 0 else None
    next_lecon = lecons[current_index + 1] if current_index < len(lecons) - 1 else None
    
    return render(request, 'tutoriel/lecon_detail.html', {
        'tutorial': tutorial,
        'lecon': lecon,
        'progression': progression,
        'prev_lecon': prev_lecon,
        'next_lecon': next_lecon,
    })

@login_required
def passer_quiz(request, quiz_id):
    """Passer un quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    lecon = quiz.lecon
    
    if request.method == 'POST':
        form = QuizForm(quiz, request.POST)
        if form.is_valid():
            # Calculer le score
            score = form.calculate_score()
            
            # Mettre à jour la progression
            progression, created = ProgressionUtilisateur.objects.update_or_create(
                utilisateur=request.user,
                tutorial=lecon.tutorial,
                lecon=lecon,
                defaults={
                    'est_completee': True,
                    'score_quiz': score,
                    'date_completion': timezone.now()
                }
            )
            
            messages.success(request, f'Quiz terminé ! Score: {score}%')
            return redirect('tutoriel:lecon_detail', 
                          tutorial_id=lecon.tutorial.id, 
                          lecon_id=lecon.id)
    else:
        form = QuizForm(quiz)
    
    return render(request, 'tutoriel/quiz.html', {
        'quiz': quiz,
        'form': form,
        'lecon': lecon,
    })

@login_required
def ma_progression(request):
    """Page de progression de l'utilisateur"""
    progressions = ProgressionUtilisateur.objects.filter(
        utilisateur=request.user
    ).select_related('tutorial', 'lecon')
    
    # Statistiques
    total_lecons = Lecon.objects.count()
    lecons_completees = progressions.filter(est_completee=True).count()
    pourcentage = int((lecons_completees / total_lecons * 100)) if total_lecons > 0 else 0
    
    # Regrouper par tutoriel
    by_tutorial = {}
    for prog in progressions:
        if prog.tutorial.id not in by_tutorial:
            by_tutorial[prog.tutorial.id] = {
                'tutorial': prog.tutorial,
                'lecons': [],
                'complete': 0,
                'total': prog.tutorial.lecons.count()
            }
        by_tutorial[prog.tutorial.id]['lecons'].append(prog)
        if prog.est_completee:
            by_tutorial[prog.tutorial.id]['complete'] += 1
    
    return render(request, 'tutoriel/progression.html', {
        'progressions': progressions,
        'by_tutorial': by_tutorial.values(),
        'stats': {
            'total_lecons': total_lecons,
            'lecons_completees': lecons_completees,
            'pourcentage': pourcentage,
        }
    })