from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<video_id>', views.single_video, name='single-video'),
]
