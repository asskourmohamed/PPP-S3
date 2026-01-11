
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def signe_vers_texte(request):
    """Page de traduction signe → texte"""
    return render(request, 'traduction/signe_vers_texte.html')

@login_required
def texte_vers_signe(request):
    """Page de traduction texte → signe"""
    return render(request, 'traduction/texte_vers_signe.html')