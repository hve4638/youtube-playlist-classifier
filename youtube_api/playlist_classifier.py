import re
import csv
import os
from .Map import *
from .youtube_api import *
from .playlist_db import *

CHANNEL_FILE: str = "data/channels.csv"
CLIENT_SECRET_KEY: str = "auth/client_secret.json"
TOKEN: str = "auth/tokens.json"

def getcondprint(cond:bool):
    return lambda s : print(s) if cond else None

class PlaylistClassifier:
    db_header = "title,channelTitle,duration,id,channelId".split(",")
    
    def __init__(self):
        self.youtube = None
        self.lastitem = {}

    def setAPI(self, youtube:YoutubeAPI):
        self.youtube = youtube
        pass

    def build(self):
        self.youtube = YoutubeAPI()
        self.youtube.build(CLIENT_SECRET_KEY, TOKEN)

    def requestPlaylistItems(self, playlist:str, exportfile:str, shared:dict = None):
        map = Map(CHANNEL_FILE)

        channelId: str = "None"
        channelTitle: str = "None"

        shared["count"] = 0
        shared["lastItem"] = item
        
        db = PlaylistDB()
        db.load(exportfile)
        try:
            ids = []
            for info in self.youtube.requestPlaylistItems(playlist, requestSize=50):
                ids.append(info["id"])

            for item in self.youtube.requestVideos(ids, requestSize=50):
                shared["count"] += 1
                shared["lastItem"] = item
                channelId = item["channelId"]
                channelTitle = item["channelTitle"]
                
                db.add(item)
                map[channelTitle] = channelId
        except HttpError as ex:
            lastitem = shared["lastItem"]

            print(f"HttpError({ex.resp.status}) {ex._get_reason()}")
            print(f"[Last Response] ({shared['count']})")
            print(f"title : {lastitem['title']}")
            print(f"titleId : {lastitem['id']}")
            print(f"channelTitle : {lastitem['channelTitle']}")
            print(f"channelId : {lastitem['channelId']}")
        except Exception as ex:
            print("Exception Occur!")
            print(f"{ex}")
        finally:
            map.save()
            db.save(exportfile)

    def classify(self, filters:list, import_dbpath:str, exportdir:str):
        exportdir = exportdir.replace("\\", "/")
        if exportdir.endswith("/"):
            exportdir = exportdir[:-1]

        classifieds = {}
        db = PlaylistDB()
        db.load(import_dbpath)
        for item in db:
            playlist = None
            for filter in filters:
                playlist = filter(item)
                if playlist is not None:
                    break
            
            
            if playlist is not None:
                classified_path = f"{exportdir}/{playlist}.csv"
            else:
                classified_path = f"{exportdir}/__NoClassify__.csv"

            if classified_path not in classifieds:
                playlistDB = PlaylistDB()
                playlistDB.load(classified_path)

                classifieds[classified_path] = playlistDB
            else:
                playlistDB = classifieds[classified_path]
            
            playlistDB.add(item)
        
        for path, db in classifieds.items():
            db.save(path)
    
    def requestInsertClassified(self, importdir:str, silent:bool=False, verbose:bool=False):
        re_csv = re.compile("(.*)[.]csv")
        vprint = getcondprint(verbose)
        sprint = getcondprint(not silent)
        vprint(f"[RequestInsertClassified] Run")

        self.createDir(importdir)

        for fname in os.listdir(importdir):
            if m := re_csv.match(fname):
                playlist = m.group(1)
                filepath = f"{importdir}/{fname}"
                vprint(f"[RequestInsertClassified] Found DBFile : '{filepath}'")

                if playlist == "__NoClassify__":
                    vprint("[RequestInsertClassified] NoClassify DB Found. continue")
                    continue

                db = PlaylistDB()
                db.load(filepath)
                ids = db.ids()
                
                vprint(f"[RequestInsertClassified] Request Insert {len(ids)} items to Playlist<{playlist}>")
                result = self.youtube.requestInsertPlaylistItem(playlist=playlist, video_ids=ids)
                ispassed, passed, failed, ex = result

                if ispassed:
                    vprint(f"[RequestInsertClassified] Insert Success : Playlist<{playlist}>")
                    vprint(f"[RequestInsertClassified] Remove DB : {filepath}")
                    os.remove(filepath)
                else:
                    sprint(f"[RequestInsertClassified] Insert Fail : Playlist<{playlist}>")
                    sprint(f"  ExceptionType: {type(ex)}")
                    sprint(f"  Reason: {ex}")
                    sprint(f"  PassCount : {len(passed)}")
                    sprint(f"  FailCount : {len(failed)}")

                    remainDB = PlaylistDB()
                    for id in failed:
                        try:
                            videoinfo = db[id]
                            remainDB.add(videoinfo)
                        except ValueError:
                            sprint(f"[Warning] id<{id}> not in PlaylistDB<{playlist}>")
                            remainDB.add({"id": id})

                    remainDB.save(filepath)
                    vprint(f"[RequestInsertClassified] Update DB ({len(db)} -> {len(remainDB)}) : {filepath}")
                    vprint(f"Break")
                    break

    def mockInsertClassified(self, importdir:str, silent:bool=False, verbose:bool=True):
        re_csv = re.compile("(.*)[.]csv")
        vprint = getcondprint(verbose)
        sprint = getcondprint(not silent)
        print(f"[MockInsertClassified] Run")

        for fname in os.listdir(importdir):
            if m := re_csv.match(fname):
                playlist = m.group(1)
                filepath = f"{importdir}/{fname}"
                print(f"[MockInsertClassified] Found DBFile : {filepath}")

                db = PlaylistDB()
                db.load(filepath)
                ids = db.ids()

                vprint(f"[MockInsertClassified] Mock Insert {len(ids)} items to Playlist<{playlist}>")
                result = self.youtube.mockInsertPlaylistItem(playlist=playlist, video_ids=ids)
                ispassed, passed, failed, ex = result
                vprint(f"  ispassed : {ispassed}")
                vprint(f"  passcount : {len(passed)}")
                vprint(f"  failcount : {len(failed)}")
    
    def removeDirFile(self, dir:str, silent:bool=False, verbose:bool=False):
        vprint = getcondprint(verbose)
        sprint = getcondprint(not silent)
        re_csv = re.compile("(.*)[.]csv")

        for fname in os.listdir(dir):
            if m := re_csv.match(fname):
                filepath = f"{dir}/{fname}"

                try:
                    os.remove(filepath)
                except PermissionError:
                    sprint(f"[RemoveDirFile] PermissionError : {filepath}")
                
                vprint(f"[RemoveDirFile] Remove file : {filepath}")

    def createDir(self, dir:str):
        if not os.path.exists(dir):
            os.makedirs(dir)