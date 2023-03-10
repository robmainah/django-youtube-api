from .functions import *
import os
from .PickleData import save_data, load_data


def get_data(params: object, filename: str, video_id=None) -> object:
    # if video_id:
    #     data = get_single_video(video_id) 
    # else:
    #     data = get_videos_data(params)
    if os.path.exists(filename):
        data = load_data(filename)
    else:
        if video_id:
            data = get_single_video(video_id)
            # save_data(filename, data)
        else:
            data = get_videos_data(params)

    return data


def get_videos_data(params: object) -> object:
    data = {**params, **{
            'part': 'snippet', 'type': 'video', 'maxResults': 10
        }}

    videos = youtube_build().search().list(**data).execute()

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
