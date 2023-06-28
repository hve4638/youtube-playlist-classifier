#!/usr/bin/env python3
from youtube_api import *
from datetime import *
import filters as Filters

CLIENT_SECRET: str = "auth/client_secret.json"
TOKEN: str = "auth/tokens.json"

if __name__ == "__main__":
    Filters.initFilter(Map("data/playlist.csv"))

    classify_filters = [
        Filters.filterMapGener(Map("data/playlistfilter.csv")),
        Filters.filterDuration,
        Filters.filterUnclassification,
    ]

    youtube = YoutubeAPI()
    youtube.build(CLIENT_SECRET, TOKEN)
    
    classifier = PlaylistClassifier()
    classifier.setAPI(youtube)
    Filters.openlogger()
    try:
        #classifier.removeDirFile(dir="classified", verbose=True)

        #classifier.classify(filters=classify_filters, import_dbpath="data/watchlaterDB.csv", exportdir="classified")
        
        # classifier.mockInsertClassified(importdir="classified", verbose=True)
        
        # classifier.requestInsertClassified(importdir="classified", verbose=True)
        pass
    finally:
        Filters.closelogger()
