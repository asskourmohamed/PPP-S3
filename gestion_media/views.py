from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_video(request):
    """Upload de vidéo (version temporaire)"""
    return JsonResponse({
        'status': 'success',
        'message': 'Upload à implémenter',
        'file_url': '/media/demo/video.mp4'
    })