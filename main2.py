from moviepy.editor import VideoFileClip
from PIL import Image

# Assurer la compatibilité avec les versions récentes de Pillow
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS


def compress_video(input_path, output_path, bitrate):
    # Charger la vidéo
    clip = VideoFileClip(input_path)

    # Sauvegarder la vidéo compressée avec l'audio et un bitrate spécifié
    clip.write_videofile(output_path, codec='libx264', bitrate=bitrate, audio=True)


if __name__ == "__main__":
    input_video = "/Users/achille/Downloads/cheminabra.mp4"  # Chemin de la vidéo d'entrée
    output_video = "/Users/achille/Downloads/chemin_output_video.mp4"  # Chemin de la vidéo de sortie
    bitrate = "500k"  # Bitrate cible (500 kbps)

    compress_video(input_video, output_video, bitrate)
