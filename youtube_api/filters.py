import os
import re
import csv
from datetime import datetime
from .filter_const import *
from .Map import *

class FilterLogger:
    def __init__(self, filename=None):
        if filename is not None:
            self.file = open(filename, "a", encoding="utf-8")
            self.writer = csv.writer(self.file)
        else:
            self.file = None
            self.writer = None

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def write(self, contents:list):
        if self.file is None:
            print(" | ".join(contents))
        else:
            self.writer.writerow(contents)

class Filter:
    def __init__(self):
        self.header = [ "CHANNEL", "CHANNEL_ID", "PLAYLIST", "PLAYLIST_ID", "PLAYLIST_REDIRECT" ]
        self.logger = FilterLogger(self.__getlogfilename())
        self.filtermap = {}
        self.playlists = {}

    def export(self, filename):
        map = Map(filename)
        for key, value in self.filtermap.items():
            map[key] = value
        map.save()

    def parse(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames

            for head in self.header:
                if head not in header:
                    raise ParseFailException(f"Filter에서 올바른 Header를 찾을 수 없습니다 : {head}")
            
            rows = []
            for row in reader:
                rows.append(row)
            
            self.playlists = self.__parsePlaylists(rows)
            self.filtermap = self.__parseChannels(rows, playlists=self.playlists)
    
    def __parsePlaylists(self, rows):
        playlistRedirect = {}
        playlist = {}
        for row in rows:
            pl_title = row["PLAYLIST"]
            pl_id = row["PLAYLIST_ID"]
            pl_redirect = row["PLAYLIST_REDIRECT"]

            if not pl_title:
                continue
            elif pl_id:
                if pl_title in playlist:
                    raise SymbolConflictException(f"심볼 충돌 '{pl_title}'")
                playlist[pl_title] = pl_id
            elif pl_redirect:
                playlistRedirect[pl_title] = pl_redirect

        for title, redirectTo in playlistRedirect.items():
            if redirectTo in playlist:
                playlist[title] = playlist[redirectTo]
            else:
                raise SymbolMissingException(f"Redirect 방향을 찾을 수 없습니다. '{title}'->'{redirectTo}'")
        return playlist

    def __parseChannels(self, rows, playlists):
        filtermap = {}

        for row in rows:
            ch_id = row["CHANNEL_ID"]
            pl_title = row["PLAYLIST"]
            pl_id = row["PLAYLIST_ID"]
            
            self.map_filter = {}
            if not ch_id:
                continue
            elif pl_title:
                filtermap[ch_id] = playlists[pl_title]
            elif pl_id:
                filtermap[ch_id] = pl_id
            else:
                # 채널이 아무 플레이리스트도 가르키지 않는 경우
                # 에러는 아님
                pass
        return filtermap

    def __getlogfilename(self):
        if not os.path.exists("log"):
            os.mkdir("log")
        now = datetime.now()
        formatted = now.strftime("%y%m%d_%H%M%S")
        return f"log/{formatted}.csv"
    
    def getMapFilter(self):
        filtermap = self.filtermap
        def filter(item, verbose=False, silent=False):
            channelId = item["channelId"]
            if channelId in filtermap:
                return filtermap[channelId]
        
        return filter
    
    def getDurationFilter(self):
        playlist_short = self.playlists["$SHORT"]
        playlist_long = self.playlists["$LONG"]
        def filter(item, verbose=False, silent=False):
            hours, minutes, seconds = self.__youtube_duration(item["duration"])
            full_minutes = ((hours*60) + minutes)
            full_sec = full_minutes * 60 + seconds

            if full_minutes >= 39:
                return playlist_long
            elif full_minutes <= 3:
                return playlist_short
            else:
                return FILTER_PASS
        return filter

    def getUnclassificationFilter(self):
        def filter(item, verbose=False, silent=False):
            contents = [
                "미분류됨",
                item["title"],
                item["id"],
                item["channelTitle"],
                item["channelId"],
            ]

            self.logger.write(contents)
            return self.playlists["$NOCLASSIFY"]
        return filter
    

    re_duration_format = re.compile("PT([0-9]|H|S|M)+")
    re_duration_h = re.compile(".*?([0-9]+)H.*?")
    re_duration_m = re.compile(".*?([0-9]+)M.*?")
    re_duration_s = re.compile(".*?([0-9]+)S.*?")
    def __youtube_duration(self, duration:str):
        hours = 0
        minutes = 0;
        seconds = 0;
        if self.re_duration_format.match(duration) is None:
            pass
        else:
            if m := self.re_duration_h.match(duration):
                hours = int(m.group(1))
            if m := self.re_duration_m.match(duration):
                minutes = int(m.group(1))
            if m := self.re_duration_s.match(duration):
                seconds = int(m.group(1))
        
        return hours, minutes, seconds
