#!/usr/bin/env python3
import csv
from youtube_api import *
from datetime import *

PLAYLIST_SHORT = None
PLAYLIST_LONG = None
PLAYLIST_UNCLASSICIFICATION = None
logger = None
logwriter = None

def openlogger():
    global logger, logwriter
    now = datetime.now()
    formatted = now.strftime("%y%m%d_%H%M%S")
    logger = open(f"log/{formatted}.csv", "w", encoding="utf-8")
    logwriter = csv.writer(logger)

def closelogger():
    logger.close()

def initFilter(map:Map):
    global PLAYLIST_SHORT, PLAYLIST_LONG, PLAYLIST_UNCLASSICIFICATION
    PLAYLIST_SHORT = map["짧"]
    PLAYLIST_LONG = map["긴거"]
    PLAYLIST_UNCLASSICIFICATION = map["미분류"]

def filterMapGener(map:Map):
    def filterMap(item, verbose=False):
        channelId = item["channelId"]
        if channelId in map:
            return map[channelId]
        
    return filterMap

def filterDuration(item, verbose=False):
    hours, minutes, seconds = youtube_duration(item["duration"])
    full_minutes = ((hours*60) + minutes)
    full_sec = full_minutes * 60 + seconds

    if full_minutes >= 40:
        return PLAYLIST_LONG
    elif full_minutes <= 3:
        return PLAYLIST_SHORT
    else:
        return None
    
def filterUnclassification(item, verbose=False):
    title = item["title"]
    id = item["id"]
    channelTitle = item["channelTitle"]
    channelId = item["channelId"]

    logger.write("")
    emsg = "미분류됨"
    logwriter.writerow([emsg, title, channelTitle, id, channelId])
    return PLAYLIST_UNCLASSICIFICATION