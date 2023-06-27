import re
import datetime
import time
import os
from .google_api import *

def build_with_credentials(credentials):
    return build("youtube", "v3", credentials=credentials)

def build_with_developerkey(devkey):
  return build("youtube", "v3", developerKey=devkey)

def youtube_get_videos_as_playlist(youtube, playlistid):
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlistid
    )
    response = request.execute()
    
    items = []
    for info in response['items']:
        item = {}
        #info['id'] = item['contentDetails']['videoId']
        item['id'] = info['contentDetails']['videoId']
        item['title'] = info['snippet']['title']
        item['channelTitle'] = info['snippet']['channelTitle']
        item['channelId'] = info['snippet']['channelId']
        items.append(item)
    return items

def get_videos(youtube, video_ids):
    request = youtube.videos().list(
        part='snippet,contentDetails',
        id=','.join(video_ids)
    )
    response = request.execute()
    
    items = []
    for i, info in enumerate(response['items']):
        item = {}
        item['id'] = video_ids[i]
        item['title'] = info['snippet']['title']
        item['duration'] = info['contentDetails']['duration']
        item['channelTitle'] = info['snippet']['channelTitle']
        item['channelId'] = info['snippet']['channelId']
        items.append(item)
    return items

def insert_playlist(youtube, playlist_id, video_ids):
    for video_id in video_ids:
        request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        response = request.execute()