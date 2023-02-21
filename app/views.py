from django.shortcuts import render
from django.http import HttpResponse
# from googleapiclient.discovery import build
import environ
import pickle
import os
from .services.SearchVideos import search_videos

env = environ.Env()
environ.Env.read_env()


def save_all_videos_to_pickle(filename, videos):
    file = open(filename, 'ab')
    pickle.dump(videos, file)
    file.close()
    

def load_all_videos_from_pickle(filename):
    file = open(filename, 'rb')
    videos = pickle.load(file)
    file.close()
    return videos


def home(request):
    filename = 'all_videos.pickle'

    if os.path.exists(filename):
        videos = load_all_videos_from_pickle(filename)
    else:
        term = 'avengers'
        videos = search_videos.search(env('YOUTUBE_API_KEY'), term)
        # print(videos['items'])
        save_all_videos_to_pickle(filename, videos)

    return render(request, 'app/index.html', {'videos': videos['items']})
    
    # return render(request, 'app/index.html')


def single_video(request, video_id):
    print("dddd", video_id)
    return render(request, 'app/detail.html')
