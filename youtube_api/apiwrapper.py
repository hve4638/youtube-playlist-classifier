from .youtube_api_procedural import *
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

    def requestVideos(self, video_ids, requestSize:int = 30):
        def request(ids):
            req = self.youtube.videos().list(
                part='snippet,contentDetails',
                maxResults=len(ids),
                id=','.join(ids)
            )
            res = req.execute()
            res_items = res['items']
            return res_items
        
        for i in range(0, len(video_ids), requestSize):
            ids = video_ids[i:i + requestSize]

            items = request(ids)
            for i, item in enumerate(items):
                yield self.__toItems(item, id=ids[i])

    def requestPlaylistItems(self, playlist:str, requestSize:int = 30):
        def request(nextPageToken=None):
            if nextPageToken is None:
                req = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist,
                    maxResults=requestSize
                )
            else:
                req = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist,
                    maxResults=requestSize,
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

    def requestInsertToPlaylist(self, playlist:str, video_ids, requestSize:int = 30):
        for i in range(0, len(video_ids), requestSize):
            ids = video_ids[i:i + requestSize]

            request = self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': ','.join(ids)
                        }
                    }
                }
            )
            response = request.execute()