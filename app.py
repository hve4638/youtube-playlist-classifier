#!/usr/bin/env python3
import ytplorderer
import plfilter
import csv

PLAYLIST_SHORT = None
PLAYLIST_LONG = "PLUE_U19elmjTA5dtEX48ei8WdQysm05uq"
PLAYLIST_UNCLASSICIFICATION = "PLUE_U19elmjRCx5QyfO67QZlVVBjjjvq6"
logger = None
logwriter = None

def filterDuration(item, verbose=False):
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

if __name__ == "__main__":
    plfilter.init()
    
    playlist = ""
    filters = [
        plfilter.yt_mapfilter,
        filterDuration,
        filterUnclassification,
    ]

    target = "PLUE_U19elmjTld6LlQnYF6nL2ewNz_XcK"

    logger = open("log.txt", "a", encoding="utf-8")
    logwriter = csv.writer(logger)

    #print(plfilter.filtermap)

    try:
        ytplorderer.init()
        ytplorderer.run(target, filters, verbose=True)
    finally:
        logger.close()
