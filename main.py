from moviepy.editor import VideoFileClip
from PIL import Image

# Assurer la compatibilité avec les versions récentes de Pillow
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

def compress_video(input_path, output_path, target_size):
    # Charger la vidéo
    clip = VideoFileClip(input_path)

    # Calculer la nouvelle taille de la vidéo
    width, height = clip.size
    new_width = int(width * target_size)
    new_height = int(height * target_size)

    # Assurer que les nouvelles dimensions sont valides
    if new_width <= 0 or new_height <= 0:
        raise ValueError("Les nouvelles dimensions de la vidéo doivent être > 0")

    # Redimensionner la vidéo
    clip_resized = clip.resize(newsize=(new_width, new_height))

    # Sauvegarder la vidéo compressée avec l'audio
    clip_resized.write_videofile(output_path, codec='libx264', bitrate='500k', audio=True)


if __name__ == "__main__":
    input_video = "/Users/achille/Downloads/cheminabra.mp4"   # Chemin de la vidéo d'entrée
    output_video = "/Users/achille/Downloads/chemin_output_video.mp4" # Chemin de la vidéo de sortie
    target_size = 0.707  # Taille cible (en pourcentage de la taille originale)

    compress_video(input_video, output_video, target_size)
