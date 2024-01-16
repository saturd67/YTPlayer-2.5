import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
YOUTUBE_API_KEY = os.environ.get('AIzaSyDdBvbYp4KaKXMK24Cq5ceRqLxMFvRUnuw')

youtube = build('youtube', 'v3',developerKey='AIzaSyDdBvbYp4KaKXMK24Cq5ceRqLxMFvRUnuw')

def search(query):
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        maxResults=20,
        type='video'
    )

    response = request.execute()

    search_results = []

    for video in response['items']:
        title = video["snippet"]["title"] 
        video_id = video["id"]["videoId"]
        item = {
            'name': title,
            'value': f'https://www.youtube.com/watch?v={video_id}',
        }

        search_results.append(item)

    return search_results