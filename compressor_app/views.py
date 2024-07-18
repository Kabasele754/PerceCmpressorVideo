import os
import ffmpeg
import subprocess
import re
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache import cache
from .models import Video
from .forms import VideoForm


@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            input_path = video.original_file.path

            # Start compression in a separate thread
            import threading
            thread = threading.Thread(target=compress_video, args=(video.id, input_path))
            thread.start()

            return JsonResponse({'status': 'success', 'video_id': video.id})
    else:
        form = VideoForm()
    return render(request, 'compressor/upload.html', {'form': form})


def compression_progress(request, video_id):
    video = Video.objects.get(id=video_id)
    if video.compressed_file:
        progress = 100
        status = 'completed'
    else:
        progress = cache.get(f'video_compression_progress_{video_id}', 0)
        status = 'compressing'
    return JsonResponse({'progress': progress, 'status': status})


def compress_video(video_id, input_path, target_size_mb=10):
    try:
        video_id = int(video_id)
    except ValueError:
        raise ValueError(f"L'ID de la vidéo doit être un nombre entier, reçu : {video_id}")

    compressed_folder = os.path.join(settings.MEDIA_ROOT, 'compressed')
    os.makedirs(compressed_folder, exist_ok=True)

    input_filename = os.path.basename(input_path)
    output_filename = f"compressed_{video_id}_{input_filename}"
    output_path = os.path.join(compressed_folder, output_filename)

    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe['streams'][0]['duration'])
    except ffmpeg.Error as e:
        raise RuntimeError(f"Erreur lors de la lecture des informations de la vidéo : {str(e)}")

    # Définir une taille cible minimale pour les vidéos longues
    if duration > 3600:  # Par exemple, pour les vidéos de plus d'une heure
        target_size_mb = max(target_size_mb, duration / 360)  # Ajuster la taille cible

    target_total_bitrate = (target_size_mb * 8192) / duration
    video_bitrate = target_total_bitrate - 128

    # Définir un bitrate vidéo minimum
    minimum_video_bitrate = 300  # En kbps
    video_bitrate = max(video_bitrate, minimum_video_bitrate)

    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path,
                           vcodec='libx264',
                           acodec='aac',
                           audio_bitrate='128k',
                           **{'b:v': f'{video_bitrate}k'})

    cmd = ffmpeg.compile(stream, overwrite_output=True)

    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)

    for line in process.stderr:
        print(line)  # Log stderr output for debugging purposes
        match = re.search(r'time=(\d{2}:\d{2}:\d{2}\.\d{2})', line)
        if match:
            time = match.group(1)
            hours, minutes, seconds = time.split(':')
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
            progress = min(100, (total_seconds / duration) * 100)
            cache.set(f'video_compression_progress_{video_id}', progress, 300)

    process.wait()

    if process.returncode != 0:
        raise RuntimeError("La compression vidéo a échoué.")

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        raise RuntimeError("Le fichier compressé n'a pas été créé correctement.")

    video = Video.objects.get(id=video_id)
    video.compressed_file = f"compressed/{output_filename}"
    video.save()

    return output_path

def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'compressor/video_list.html', {'videos': videos})


def stream_video(request, video_id):
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"Contenu du dossier media:")
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        level = root.replace(settings.MEDIA_ROOT, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return HttpResponse(f"Vidéo avec l'ID {video_id} non trouvée.", status=404)

    if not video.compressed_file:
        return HttpResponse("Le fichier compressé n'existe pas encore.", status=404)

    relative_path = str(video.compressed_file)
    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    print(f"Chemin absolu du fichier : {absolute_path}")
    print(f"Le fichier existe : {os.path.exists(absolute_path)}")

    if not os.path.exists(absolute_path):
        return HttpResponse(f"Fichier non trouvé: {relative_path}", status=404)

    file_size = os.path.getsize(absolute_path)

    def file_iterator(file_name, chunk_size=8192):
        with open(file_name, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    response = StreamingHttpResponse(file_iterator(absolute_path))
    response['Content-Type'] = 'video/mp4'
    response['Content-Length'] = file_size
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(absolute_path)}"'
    return response
