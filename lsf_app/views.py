
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ProfilForm

def inscription(request):
    """Vue pour l'inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Connecter automatiquement l'utilisateur
            login(request, user)
            
            messages.success(request, 'Inscription réussie ! Bienvenue sur LSF Connect.')
            return redirect('accueil')
    else:
        form = InscriptionForm()
    
    return render(request, 'compte/inscription.html', {'form': form})

@login_required
def profil(request):
    """Vue pour afficher et modifier le profil"""
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour.')
            return redirect('compte:profil')
    else:
        form = ProfilForm(instance=request.user)
    
    return render(request, 'compte/profil.html', {'form': form})