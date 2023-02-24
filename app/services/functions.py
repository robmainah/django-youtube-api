from datetime import datetime
from googleapiclient.discovery import build
import environ


env = environ.Env()
environ.Env.read_env()


def youtube_build():
    return build('youtube', 'v3', developerKey=env('YOUTUBE_API_KEY'))


def get_channel_data(channel_ids):
    return youtube_build().channels().list(
        id=channel_ids, part='snippet', maxResults=50
    ).execute()


def get_channel_ids(videos):
    return [video['snippet']['channelId'] for video in videos]


def get_video_data(video_ids):
    return youtube_build().videos().list(
        id=video_ids, part='statistics, contentDetails',
    ).execute()


def get_video_ids(videos):
    return [video['id']['videoId'] for video in videos]


def get_channel_index(video, channels_data):
    for element, channel in enumerate(channels_data['items']):
        if channel['id'] == video['snippet']['channelId']:
            return element
    return None


def get_video_index(video, videos_data):
    for element, channel in enumerate(videos_data['items']):
        if channel['id'] == video['id']['videoId']:
            return element
    return None


def parse_datetime(date_time):
    return datetime.fromisoformat(date_time)

