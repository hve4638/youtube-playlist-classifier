from Map import *

CHANNEL_FILE: str = "data/channels.csv"
PLAYLIST_FILE: str = "data/playlist.csv"

filtermap = {}

def init():
    channels = Map(CHANNEL_FILE)
    playlists = Map(PLAYLIST_FILE)

    MAIN = playlists["MAIN"]
    LONG = playlists["LONG"]
    VTUBER = playlists["VTUBER"]
    TECH = playlists["테크"]
    REVIEW = playlists["리뷰"]
    KNOW = playlists["지식"]

    filtermap[channels["침착맨"]] = playlists["침착맨"]
    filtermap[channels["슈카월드"]] = playlists["슈카"]

    filtermap[channels["안될공학 - IT 테크 신기술"]] = TECH

    filtermap[channels["테크기어캐스트 Tech Gear Cast"]] = REVIEW
    filtermap[channels["게임장비리뷰 겜용이"]] = REVIEW
    filtermap[channels["Luv IT ATO  러빗아토"]] = REVIEW
    #filtermap[channels[""]] = REVIEW
    
    filtermap[channels["지식한입"]] = KNOW
    filtermap[channels["지식해적단"]] = KNOW
    #filtermap[channels[""]] = KNOW

    filtermap[channels["침착맨 플러스"]] = LONG

    filtermap[channels["여까네 유튜브"]] = MAIN
    filtermap[channels["똘똘똘이의 유튜브"]] = MAIN
    filtermap[channels["김도랜드"]] = MAIN
    filtermap[channels["중년게이머 김실장"]] = MAIN
    filtermap[channels["김나성"]] = MAIN
    #filtermap[channels[""]] = MAIN

    filtermap[channels["클립애호가 Clip Devotee"]] = VTUBER
    filtermap[channels["홀로스터딩"]] = VTUBER
    filtermap[channels["호소이누"]] = VTUBER
    filtermap[channels["오리고기"]] = VTUBER
    filtermap[channels["하타치"]] = VTUBER
    filtermap[channels["버튜버 팬박스"]] = VTUBER
    filtermap[channels["허니츄러스 HoneyChurros"]] = VTUBER
    filtermap[channels["고등어 Ch."]] = VTUBER
    filtermap[channels["호소이누 Hosoinu"]] = VTUBER
    filtermap[channels["물색의별[Mulsec]"]] = VTUBER
    filtermap[channels["하타치 Hatachi"]] = VTUBER
    filtermap[channels["오리고기 ORIGOGI"]] = VTUBER
    #filtermap[channels[""]] = VTUBER

def yt_mapfilter(item, verbose = False):
    channelId = item['channelId']
    
    playlist = None
    if channelId in filtermap:
        playlist = filtermap[channelId]

    if verbose:
        print(f"[MapFilter] {channelId} -> {playlist}")

    return playlist