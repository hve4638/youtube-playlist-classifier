#!/usr/bin/env python3
import os
import argparse
from youtube_api import *
from datetime import *
from proc import *

def getopparser():
    parser = argparse.ArgumentParser(description="OP")
    parser.add_argument("-a", "--authentication", dest="authentication", help="", action="store_true")
    parser.add_argument("-s", "--scan", dest="scan", help="")
    parser.add_argument("-d", "--delete-playlist", dest="delete_playlist", help="")
    parser.add_argument("-c", "--classify", dest="classify", help="", action="store_true")
    parser.add_argument("-i", "--insert", dest="insert", help="", action="store_true")
    parser.add_argument("-w", "--workingdirectory", dest="workingdirectory", help="", action="store_true")
    parser.add_argument("-v", "--validation", dest="validation", help="", action="store_true")
    parser.add_argument("--clear", dest="clear_process", help="Clear", action="store_true")
    parser.add_argument("--get-channels", dest="get_channels", help="Export Channels Info while Read playlist")
    parser.add_argument("--get-channels-noclassify", dest="get_channels_noclassify", help="Export Channels Info while Read playlist without Classified")
    parser.add_argument("--get-filter", dest="get_filter", help="Get current filter")
    parser.add_argument("--set-filter", dest="set_filter", help="Set filter")
    parser.add_argument("--refresh-auth", dest="refresh_auth", help="Refresh Auth", action="store_true")

    parser.add_argument("--mock", dest="mock", help="Mock mode", action="store_true")
    parser.add_argument("--verbose", dest="verbose", help="verbose", action="store_true")
    parser.add_argument("--silent", dest="silent", help="silent", action="store_true")

    return parser

if __name__ == "__main__":
    nowork = True
    parser = getopparser()
    args = parser.parse_args()

    if not validation():
        exit(-1)

    verbose = args.verbose
    silent = args.silent

    if args.workingdirectory:
        os.chdir(WORKING_DIRECTORY)

    if args.refresh_auth:
        removeYoutubeToken()
        initYoutube()

    if args.authentication:
        initYoutube()

    if args.get_filter:
        getfilter(args.get_filter)

    if args.set_filter:
        setfilter(args.set_filter)

    if args.clear_process:
        classifier.removeDirFile(dir="classified", verbose=True)

    if args.scan:
        readPlaylist(args.scan, verbose=verbose, silent=silent)
        
    if args.delete_playlist:
        deletePlaylist(args.delete_playlist, verbose=verbose, silent=silent)

    if args.get_channels:
        getchannels(args.get_channels)

    if args.get_channels_noclassify:
        getchannelsNoClassified(args.get_channels_noclassify)

    if args.classify:
        classify(verbose=verbose, silent=silent)
    
    if args.insert:
        insertPlaylist(verbose=verbose, silent=silent)
