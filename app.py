#!/usr/bin/env python3
import os
import argparse
from youtube_api import *
from datetime import *
nowork = False

CLIENT_SECRET: str = "auth/client_secret.json"
TOKEN: str = "auth/tokens.json"

FILE_FILTER = "data/filtermap.csv"
FILE_PLAYLIST = "data/playlistitems.csv"
DIR_CLASSIFY = "classified"

builded = False
youtube = YoutubeAPI()
classifier = PlaylistClassifier(youtube)

def initYoutube():
    global builded
    if not builded:
        youtube.build(CLIENT_SECRET, TOKEN)
        builded = True

def getopparser():
    parser = argparse.ArgumentParser(description="OP")
    parser.add_argument("-a", "--authentication", dest="authentication", help="", action="store_true")
    parser.add_argument("-r", "--read", dest="read", help="")
    parser.add_argument("-c", "--classify", dest="classify", help="", action="store_true")
    parser.add_argument("-i", "--insert", dest="insert", help="", action="store_true")
    parser.add_argument("-v", "--verbose", dest="verbose", help="verbose", action="store_true")
    parser.add_argument("-s", "--silent", dest="silent", help="silent", action="store_true")
    parser.add_argument("--clear", dest="clear_process", help="Clear", action="store_true")
    parser.add_argument("-m", "--make-filter", dest="make_filter", help="Make Filter (need -o option)")
    parser.add_argument("-o", "--output", dest="output", help="Output file")
    parser.add_argument("--get-channels", dest="get_channels", help="Export Channels Info while Read playlist")
    parser.add_argument("--get-filter", dest="get_filter", help="Get current filter")
    parser.add_argument("--set-filter", dest="set_filter", help="Set filter")
    parser.add_argument("--mock", dest="mock", help="Mock mode")

    return parser

def input_boolean(prompt:str):
    while True:
        print(prompt, end="")
        y = input()
        if y == "Y" or y == "y":
            return True
        elif y == "n":
            return False

def makeFilter(filename, output):
    filter = Filter()
    filter.parse(filename)
    filter.export(output)

def getfilter(filename):
    os.system(f"cp {FILE_FILTER} {filename}")

def setfilter(filename):
    os.system(f"cp {filename} {FILE_FILTER}")

def getchannels(filename):
    os.system(f"cp {CHANNEL_FILE} {filename}")

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

if __name__ == "__main__":
    nowork = True
    parser = getopparser()
    args = parser.parse_args()

    verbose = args.verbose
    silent = args.silent

    if args.authentication:
        initYoutube()
        nowork = False

    if args.get_filter:
        getfilter(args.get_filter)
        nowork = False

    if args.set_filter:
        setfilter(args.set_filter)
        nowork = False

    if args.clear_process:
        classifier.removeDirFile(dir="classified", verbose=True)
        nowork = False

    if args.read:
        readPlaylist(args.read, verbose=verbose, silent=silent)
        nowork = False

    if args.get_channels:
        getchannels(args.get_channels)
        nowork = False

    if args.classify:
        classify(verbose=verbose, silent=silent)
        nowork = False
    if args.insert:
        insertPlaylist(verbose=verbose, silent=silent)
        nowork = False
    
    if nowork:
        parser.print_help()
