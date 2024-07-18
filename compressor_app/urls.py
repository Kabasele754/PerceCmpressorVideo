from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.upload_video, name='upload_video'),
    path('compression-progress/<int:video_id>/', views.compression_progress, name='compression_progress'),
    path('stream-video/<int:video_id>/', views.stream_video, name='stream_video'),
]
