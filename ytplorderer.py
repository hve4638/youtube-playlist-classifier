from Map import *
from youtube_api import *
import ytplorderer
import plfilter

CHANNEL_FILE: str = "data/channels.csv"
CLIENT_SECRET_KEY: str = "auth/client_secret.json"
TOKEN: str = "auth/tokens.json"
youtube: YoutubeAPI = None

def init():
    global youtube
    youtube = YoutubeAPI()
    youtube.build(CLIENT_SECRET_KEY, TOKEN)

def run(playlist:str, filters:dict, verbose:bool = False):
    map = Map(CHANNEL_FILE)
    
    count:int = 0
    id:str = "None"
    title: str = "None"
    duration: str = "None"
    channelId: str = "None"
    channelTitle: str = "None"
    try:
        for info in youtube.requestPlaylistItems(playlist):
            id = info["id"]
            for item in youtube.requestVideos([ id ]):
                count += 1
                title = item["title"]
                duration = item["duration"]
                channelId = item["channelId"]
                channelTitle = item["channelTitle"]
                map[channelTitle] = channelId

                pl = None
                for filter in filters:
                    pl = filter(item, verbose=verbose)
                    if pl is not None:
                        break
                
                if pl is not None:
                    youtube.requestInsertToPlaylist(pl, [ id ])
                
                if verbose:
                    print(f"title: {title} ({id})")
                    print(f"channel : {channelTitle} ({channelId})")
                    print(f"duration : {duration}")
                    print(f"toPlaylist : {pl}")
                    print("-"*50)
                else:
                    print(f"[{title}]")
    except HttpError as ex:
        print(f"HttpError({ex.resp.status}) {ex._get_reason()}")
        print(f"[Last Response] ({count})")
        print(f"title : {title}")
        print(f"titleId : {id}")
        print(f"channelTitle : {channelTitle}")
        print(f"channelId : {channelId}")
    finally:
        map.save()

