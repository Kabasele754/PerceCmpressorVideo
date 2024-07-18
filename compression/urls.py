from django.urls import path

from compression.views import upload_view, video_view, compress_video

urlpatterns = [
    path('upload/', upload_view, name='compress_videos'),
    path('upload-video/', compress_video, name='compress_video'),
    path('videos/', video_view, name='video_list'),
]
