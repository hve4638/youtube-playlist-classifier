import csv
from Map import *
from youtube_api import *
from playlistdb import *

CHANNEL_FILE: str = "data/channels.csv"
CLIENT_SECRET_KEY: str = "auth/client_secret.json"
TOKEN: str = "auth/tokens.json"
youtube: YoutubeAPI = None

DBHEADER = "title,channelTitle,duration,id,channelId".split(",")

def init():
    global youtube
    youtube = YoutubeAPI()
    youtube.build(CLIENT_SECRET_KEY, TOKEN)

def runStore(playlist:str, exportfile:str):
    map = Map(CHANNEL_FILE)

    count:int = 0
    id:str = "None"
    title: str = "None"
    duration: str = "None"
    channelId: str = "None"
    channelTitle: str = "None"
    
    db = PlaylistDB()
    db.load(exportfile)

    f = open(exportfile, "w", encoding="utf-8")
    fwriter = csv.writer(f)
    try:
        ids = []
        for info in youtube.requestPlaylistItems(playlist, requestSize=50):
            ids.append(info["id"])

        for item in youtube.requestVideos(ids, requestSize=50):
            count += 1
            id = item["title"]
            title = item["title"]
            duration = item["duration"]
            channelId = item["channelId"]
            channelTitle = item["channelTitle"]
            
            db.add(item)
            map[channelTitle] = channelId
    except HttpError as ex:
        print(f"HttpError({ex.resp.status}) {ex._get_reason()}")
        print(f"[Last Response] ({count})")
        print(f"title : {title}")
        print(f"titleId : {id}")
        print(f"channelTitle : {channelTitle}")
        print(f"channelId : {channelId}")
    finally:
        f.close()
        map.save()
        db.save(exportfile)

def runClassifierMock(filters:list, importfile:str):
    db = PlaylistDB()
    db.load(importfile)
    for item in db:
        playlist = None
        for filter in filters:
            playlist = filter(item)
            if playlist is not None:
                break
        
        if playlist is not None:
            with open(f"mock/{playlist}.csv", "a", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=DBHEADER)
                writer.writerow(item)
        else:
            with open(f"mock/None.csv", "a", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=DBHEADER)
                writer.writerow(item)

def runClassifier(filters:list, importfile:str):
    db = PlaylistDB()
    db.load(importfile)
    try:
        for item in db:
            playlist = None
            for filter in filters:
                playlist = filter(item)
                if playlist is not None:
                    break
            
            if playlist is not None:
                youtube.requestInsertToPlaylist(playlist, [ item["id"] ])
    except HttpError as ex:
        print(f"HttpError({ex.resp.status}) {ex._get_reason()}")
        print(f"[Item] {item}")

def runFull(playlist:str, filters:dict, verbose:bool = False):
    map = Map(CHANNEL_FILE)
    
    count:int = 0
    id:str = "None"
    title: str = "None"
    duration: str = "None"
    channelId: str = "None"
    channelTitle: str = "None"
    try:
        for info in youtube.requestPlaylistItems(playlist, maxResults=50):
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

