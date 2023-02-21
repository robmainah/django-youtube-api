from django.shortcuts import render
# from django.http import HttpResponse
import pickle
import os
import environ
from googleapiclient.discovery import build


env = environ.Env()
environ.Env.read_env()

def save_data_to_pickle(filename, videos):
    file = open(filename, 'ab')
    pickle.dump(videos, file)
    file.close()
    

def load_data_from_pickle(filename):
    file = open(filename, 'rb')
    videos = pickle.load(file)
    file.close()
    return videos


def home(request):
    filename = 'videos_data.pickle'

    if os.path.exists(filename):
        videos = load_data_from_pickle(filename)
    else:
        term = 'avengers'
        youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
        videos = youtube.search().list(
            q=term,
            part='snippet',
            type='video',
            maxResults=50
        ).execute()

        # print(videos['items'])
        save_data_to_pickle(filename, videos)

    return render(request, 'app/index.html', {'videos': videos['items']})
    
    # return render(request, 'app/index.html')


def single_video(request, video_id):
    filename = f'video_{video_id}.pickle'

    if os.path.exists(filename):
        video = load_data_from_pickle(filename)
    else:
        youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
        video = youtube.videos().list(
            part='snippet, statistics, player',
            id=video_id,
            maxResults=1,
        ).execute()

        print(video['items'])
        save_data_to_pickle(filename, video)

    return render(request, 'app/detail.html', {'video': video['items'][0]})

    # return render(request, 'app/detail.html')
