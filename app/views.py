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


def get_video_channel_data(channel_ids):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    return youtube.channels().list(
        id=channel_ids, part='snippet', maxResults=50
    ).execute()


def get_video_data(video_ids):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    return youtube.videos().list(
        id=video_ids, part='statistics'
    ).execute()


def get_channel_ids(videos):
    return [video['snippet']['channelId'] for video in videos]


def get_video_ids(videos):
    return [video['id']['videoId'] for video in videos]


def get_channel_index(video, channels_data):
    for element, channel in enumerate(channels_data['items']):
        if channel['id'] == video['snippet']['channelId']:
            return element
    return None
    # return next((element for element, channel in enumerate(channels_data['items']) if channel['id'] == video['snippet']['channelId']), None)


def get_video_index(video, videos_data):
    for element, channel in enumerate(videos_data['items']):
        if channel['id'] == video['id']['videoId']:
            return element
    return None
    # return next((element for element, channel in enumerate(channels_data['items']) if channel['id'] == video['snippet']['channelId']), None)


def get_videos_data(term):
    youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
    videos = youtube.search().list(
        part='snippet', type='video', q=term, maxResults=50
    ).execute()

    channels_data = get_video_channel_data((',').join(get_channel_ids(videos['items'])))
    videos_data = get_video_data((',').join(get_video_ids(videos['items'])))

    for video in videos['items']:
        video['channelData'] = channels_data['items'][get_channel_index(video, channels_data)]
        video['videoData'] = videos_data['items'][get_video_index(video, videos_data)]
        video['snippet']['publishTime'] = parse_datetime(video['snippet']['publishTime'])

    return videos

def home(request):
    term = 'avengers'
    filename = f'videos_{term}_data.pickle'

    if os.path.exists(filename):
        videos = load_data_from_pickle(filename)
    else:
        videos = get_videos_data(term)
        save_data_to_pickle(filename, videos)

    return render(request, 'app/index.html', {'videos': videos})


def single_video(request, video_id):
    filename = f'video_{video_id}.pickle'

    if os.path.exists(filename):
        video = load_data_from_pickle(filename)
    else:
        youtube = build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))
        video = youtube.videos().list(
            part='contentDetails, snippet, statistics, player', id=video_id, maxResults=1,
        ).execute()

        video['items'][0]['channelData'] = get_video_channel_data(video['items'][0]['snippet']['channelId'])['items'][0]
        video['items'][0]['snippet']['publishedAt'] = parse_datetime(video['items'][0]['snippet']['publishedAt'])

        save_data_to_pickle(filename, video)

    return render(request, 'app/detail.html', {'video': video['items'][0]})


def search(request):
    term = request.GET.get('q') # + " -citizen -ntv"
    filename = f"videos_{term.replace(' ', '_')}_data.pickle"

    if os.path.exists(filename):
        videos = load_data_from_pickle(filename)
    else:
        videos = get_videos_data(term)
        save_data_to_pickle(filename, videos)

    return render(request, 'app/search.html', {'videos': videos, 'search': term})
