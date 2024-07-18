from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Video
from moviepy.editor import VideoFileClip
import os

from django.conf import settings


def check_compression_status(request):
    # Chemin où sont stockées les vidéos compressées
    compressed_dir = os.path.join(settings.MEDIA_ROOT, 'compressed')

    # Exemple de nom de fichier compressé (à adapter selon ton application)
    compressed_filename = 'video_compressed.mp4'

    # Chemin complet du fichier compressé
    compressed_path = os.path.join(compressed_dir, compressed_filename)

    # Vérifie si le fichier compressé existe
    if os.path.exists(compressed_path):
        status = {'compression_status': 'complete'}
    else:
        status = {'compression_status': 'in_progress'}

    return JsonResponse(status)


def compress_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']

        # Sauvegarde temporaire de la vidéo
        temp_video_path = os.path.join(settings.MEDIA_ROOT, 'temp', video_file.name)
        with open(temp_video_path, 'wb+') as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)

        # Chemin de sortie pour la vidéo compressée
        output_path = os.path.join(settings.MEDIA_ROOT, 'compressed', video_file.name)

        # Compression de la vidéo
        clip = VideoFileClip(temp_video_path)
        bitrate = "500k"  # Ajuste le bitrate comme nécessaire
        clip.write_videofile(output_path, codec='libx264', bitrate=bitrate, audio=True)

        # Suppression du fichier temporaire
        os.remove(temp_video_path)

        # URL de la vidéo compressée
        compressed_url = os.path.join(settings.MEDIA_URL, 'compressed', video_file.name)

        return JsonResponse({'success': True, 'compressed_url': compressed_url})

    return JsonResponse({'success': False})


@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        video_file = request.FILES['video_file']
        title = request.POST.get('title', 'Untitled')

        video_instance = Video(video_file=video_file, title=title)
        video_instance.save()

        input_path = video_instance.video_file.path
        output_path = os.path.join(settings.MEDIA_ROOT, 'videos/compressed', video_instance.video_file.name)

        # Compression logic
        clip = VideoFileClip(input_path)
        bitrate = "500k"  # You can adjust this as needed
        clip.write_videofile(output_path, codec='libx264', bitrate=bitrate, audio=True)

        # Update video instance with compressed file path
        video_instance.compressed_file = 'videos/compressed/' + video_instance.video_file.name
        video_instance.save()

        return JsonResponse({'compressed_file': video_instance.compressed_file})

    return render(request, 'compression/upload.html')

def video_view(request):
    return render(request, 'compression/video.html')
