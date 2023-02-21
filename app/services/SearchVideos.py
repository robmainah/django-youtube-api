from googleapiclient.discovery import build


class search_videos:
    def search(developer_key, term):
        youtube = build('youtube', 'v3', developerKey=developer_key)
        request = youtube.search().list(
            q=term,
            part='snippet',
            maxResults=2
        ).execute()

        return request
