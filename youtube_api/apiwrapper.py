from .youtube_api import *
from .credentials import *

class YoutubeAPI:
    def __init__(self):
        self.creds = None
        self.youtube = None
    
    def build(self, client_secret:str, token_file:str):
        self.creds = make_creds(client_secret, token_file)
        self.youtube = build_with_credentials(self.creds)

    def __toItems(self, info, id=None, duration=None):
        item = {}
        if id is None:
            id = info['contentDetails']['videoId']
        item['id'] = id
        item['title'] = info['snippet']['title']
        if duration is None:
            duration = info['contentDetails']['duration']
        item['duration'] = duration
        item['channelTitle'] = info['snippet']['channelTitle']
        item['channelId'] = info['snippet']['channelId']
        return item

    def requestVideos(self, video_ids, maxResults:int = 5):
        for video_id in video_ids:
            request = self.youtube.videos().list(
                part='snippet,contentDetails',
                id=video_id
            )

            response = request.execute()
            for item in response["items"]:
                yield self.__toItems(item, id=video_id)

    def requestPlaylistItems(self, playlist:str, maxResults:int = 5):
        def request(nextPageToken=None):
            if nextPageToken is None:
                req = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist,
                    maxResults=maxResults
                )
            else:
                req = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist,
                    maxResults=maxResults,
                    pageToken=nextPageToken
                )
            res = req.execute()
            res_items = res['items']
            res_nextpage_token = res.get('nextPageToken')
            return res_items, res_nextpage_token
        
        nextPageToken = None
        while True:
            items, nextPageToken = request(nextPageToken)
            for item in items:
                yield self.__toItems(item, duration="-")
            if nextPageToken is None:
                break
    
    def requestInsertToPlaylist(self, playlist:str, video_ids):
        for video_id in video_ids:
            request = self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            )
            response = request.execute()