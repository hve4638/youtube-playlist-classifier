#!/usr/bin/env python3
import os
from time import sleep
import sys
from youtube_api import *
from datetime import *

WORKING_DIRECTORY:str = os.path.dirname(os.path.abspath(__file__))

CLIENT_SECRET: str = f"{WORKING_DIRECTORY}/auth/client_secret.json"
TOKEN: str = f"{WORKING_DIRECTORY}/auth/tokens.json"

FILE_FILTER = f"{WORKING_DIRECTORY}/data/filtermap.csv"
FILE_PLAYLIST = f"{WORKING_DIRECTORY}/data/playlistitems.csv"
DIR_CLASSIFY = f"{WORKING_DIRECTORY}/classified"

CHANNEL_FILE: str = f"{WORKING_DIRECTORY}/data/channels.csv"

builded = False
youtube = YoutubeAPI()
classifier = PlaylistClassifier(youtube=youtube, channelfile=CHANNEL_FILE)

def validation():
    if not os.path.exists(CLIENT_SECRET):
        sys.stderr.write(f"Error: client_secret file does not exists. {CLIENT_SECRET}\n")
        exit(-1)
    else:
        return True

def removeYoutubeToken():
    os.remove(TOKEN)

def initYoutube():
    global builded
    if not builded:
        youtube.build(CLIENT_SECRET, TOKEN)
        builded = True

def input_boolean(prompt:str):
    while True:
        print(prompt, end="")
        y = input()
        if y == "Y" or y == "y":
            return True
        elif y == "n":
            return False

def getfilter(filename):
    os.system(f"cp {FILE_FILTER} {filename}")

def setfilter(filename):
    os.system(f"cp {filename} {FILE_FILTER}")

def getchannels(filename):
    os.system(f"cp {CHANNEL_FILE} {filename}")

def getchannelsNoClassified(filename:str):
    filter = Filter()
    filter.parse(FILE_FILTER)
    classify = filter.getMapFilter()

    map = Map(CHANNEL_FILE)
    noclassified = Map(filename, newfile=True)
    for key, value in map:
        if not classify({"channelId" : value }):
            noclassified[key] = value
    
    noclassified.save()

def readPlaylist(playlist:str, verbose:bool, silent:bool):
    initYoutube()
    print(f"Read Playlist.")
    item = youtube.requestPlaylist(playlist)

    if not item:
        print(f"playlist not found '{playlist}'")
        print("Exit")
        exit(-1)
    else:
        title = item['title']
        publishedAt = item['publishedAt']
        channelTitle = item['channelTitle']
        print(f"playlistInfo")
        print(f'  id : "{playlist}"')
        print(f'  title : "{title}"')
        print(f'  publishedAt : "{publishedAt}"')
        print(f'  channel : "{channelTitle}"')
        print("Are you sure? ", end="")
        if input_boolean("[Y/n] "):
            shared = {}
            classifier.requestPlaylistItems(playlist, exportfile=FILE_PLAYLIST, shared=shared)
        else:
            print("Exit")
            exit(0)

def deletePlaylist(playlist:str, verbose:bool, silent:bool):
    initYoutube()
    print("#"*30)
    print(f"Delete Playlist items.")
    print("#"*30)
    item = youtube.requestPlaylist(playlist)
    title = item['title']
    publishedAt = item['publishedAt']
    channelTitle = item['channelTitle']
    print(f"playlistInfo")
    print(f'  id : "{playlist}"')
    print(f'  title : "{title}"')
    print(f'  publishedAt : "{publishedAt}"')
    print(f'  channel : "{channelTitle}"')
    print("Do you want to continue? ", end="")
    if input_boolean("[Y/n] "):
        print("deleting...")
        sleep(3)
        
        youtube.requestDeletePlaylistItems(playlist)

def classify(importfname:str = None, exportdir:str = None, verbose:bool = False, silent:bool = False):
    filter = Filter()
    filter.parse(FILE_FILTER)
    
    classify_filters = [
        filter.getMapFilter(),
        filter.getDurationFilter(),
        filter.getUnclassificationFilter(),
    ]
    classifier.classify(filters=classify_filters, import_dbpath=FILE_PLAYLIST, exportdir=DIR_CLASSIFY)

def insertPlaylist(verbose:bool, silent:bool):
    initYoutube()
    classifier.requestInsertClassified(importdir=DIR_CLASSIFY, verbose=verbose)

def insertPlaylistMock(verbose:bool, silent:bool):
    classifier.mockInsertClassified(importdir=DIR_CLASSIFY, verbose=verbose)
