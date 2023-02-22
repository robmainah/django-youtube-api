from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
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


def parse_datetime(date_time):
    return datetime.fromisoformat(date_time)


def get_video_channel_data(channel_id):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    return youtube.channels().list(
        id=channel_id, part='snippet',
    ).execute()
    

def home(request):
    filename = 'videos_data.pickle'

    if os.path.exists(filename):
        videos = load_data_from_pickle(filename)
    else:
        term = 'avengers'
        youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
        videos = youtube.search().list(
            part='snippet', type='video', q=term, maxResults=50
        ).execute()        

        for video in videos['items']:
            video['channelData'] = get_video_channel_data(video['snippet']['channelId'])['items'][0]
            # print(video['channelData'])
            video['snippet']['publishTime'] = parse_datetime(video['snippet']['publishTime'])

        save_data_to_pickle(filename, videos)

    return render(request, 'app/index.html', {'videos': videos})
    
    # return render(request, 'app/index.html')


def single_video(request, video_id):
    filename = f'video_{video_id}.pickle'

    if os.path.exists(filename):
        video = load_data_from_pickle(filename)
    else:
        youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
        video = youtube.videos().list(
            part='snippet, statistics, player', id=video_id, maxResults=1,
        ).execute()

        # print(video['items'])
        save_data_to_pickle(filename, video)

    return render(request, 'app/detail.html', {'video': video['items'][0]})

    # return render(request, 'app/detail.html')


def search(request):
    term = request.GET.get('q') # + " -citizen -ntv"
    filename = f"videos_{term}_data.pickle"

    if os.path.exists(filename):
        videos = load_data_from_pickle(filename)
    else:        
        youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
        videos = youtube.search().list(
            part='snippet', type='video', q=term, maxResults=10
        ).execute()

        for video in videos['items']:
            video['channelData'] = get_video_channel_data(video['snippet']['channelId'])['items'][0]
            # print(video['channelData'])
            video['snippet']['publishTime'] = parse_datetime(video['snippet']['publishTime'])

        save_data_to_pickle(filename, videos)

    return render(request, 'app/search.html', {'videos': videos, 'search': term})

    return render(request, 'app/search.html')
