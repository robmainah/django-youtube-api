from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('video/<video_id>', views.single_video, name='single-video'),
]
