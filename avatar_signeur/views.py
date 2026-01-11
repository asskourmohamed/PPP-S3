
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def generate_avatar(request):
    """Génère une animation d'avatar (version temporaire)"""
    return JsonResponse({
        'status': 'success',
        'message': 'Fonction à implémenter',
        'animation_url': '/media/demo/animation.gif'
    })