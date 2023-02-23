from .functions import *
import os
from .PickleData import save_data, load_data


def get_data(term: str, filename: str, video_id=None) -> object:
    if os.path.exists(filename):
        data = load_data(filename)
    else:
        data = get_single_video(video_id) if video_id else get_videos_data(term)
        save_data(filename, data)

    return data


def get_videos_data(term: str) -> object:
    videos = youtube_build().search().list(
        part='snippet', type='video', q=term, maxResults=50
    ).execute()

    channels_data = get_channel_data((',').join(get_channel_ids(videos['items'])))
    videos_data = get_video_data((',').join(get_video_ids(videos['items'])))

    for video in videos['items']:
        video['channelData'] = channels_data['items'][get_channel_index(video, channels_data)]
        video['videoData'] = videos_data['items'][get_video_index(video, videos_data)]
        video['snippet']['publishTime'] = parse_datetime(video['snippet']['publishTime'])

    return videos


def get_single_video(video_id: str) -> object:
    video = youtube_build().videos().list(
        part='contentDetails, snippet, statistics, player', id=video_id, maxResults=1,
    ).execute()

    channel_data = get_channel_data(video['items'][0]['snippet']['channelId'])

    video['items'][0]['channelData'] = channel_data['items'][0]
    video['items'][0]['snippet']['publishedAt'] = parse_datetime(video['items'][0]['snippet']['publishedAt'])

    return video
