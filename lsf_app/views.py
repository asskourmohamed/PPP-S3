from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import InscriptionForm, ProfilForm

def connexion(request):
    """Vue pour la connexion utilisateur"""
    if request.user.is_authenticated:
        # Si déjà connecté, rediriger vers l'accueil
        return redirect('accueil')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Connexion réussie ! Bienvenue {username}.')
                
                # Rediriger vers la page demandée (next) ou l'accueil
                next_url = request.POST.get('next', 'accueil')
                return redirect(next_url)
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()
    
    # Récupérer l'URL de redirection si présente dans les paramètres GET
    next_url = request.GET.get('next', '')
    
    return render(request, 'compte/login.html', {
        'form': form,
        'next': next_url
    })

def inscription(request):
    """Vue pour l'inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('accueil')
        
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