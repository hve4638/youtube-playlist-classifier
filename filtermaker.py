#!/usr/bin/env python3
from Map import *

CHANNEL_FILE: str = "data/channels.csv"
PLAYLIST_FILE: str = "data/playlist.csv"
PLAYLIST_FILTER: str = "data/playlistfilter.csv"

def raiseEx(key):
    if len(key):
        raise Exception(f"Invalid Key '{key}'")
    else:
        return ""
        

def makeChannelFilterMap():
    filtermap = Map(PLAYLIST_FILTER)

    channels = Map(CHANNEL_FILE)
    playlists = Map(PLAYLIST_FILE)
    channels.defGetCaller = raiseEx
    playlists.defGetCaller = raiseEx

    MAIN = playlists["주"]
    SUB = playlists["부"]
    SHORT = playlists["짧"] 
    LONG = playlists["긴거"]
    LONGLONG = playlists["더긴거"]
    VTUBER = playlists["버튜버"]
    TECH = playlists["테크"]
    REVIEW = playlists["리뷰"]
    KNOW = playlists["지식"]
    CODING = playlists["코딩"]
    UTIL = playlists["유용"]
    ENG = playlists["영어"]
    MUSIC = playlists["음악"]
    NEWS = playlists["뉴스"]
    TECHSHORT = playlists["짧테크"]
    TVREPLAY = playlists["TV다시보기"]
    CPUSTUDY = playlists["컴공부"]
    CLIP = playlists["클립"]

    filtermap[channels["침착맨"]] = playlists["침착맨"]
    filtermap[channels["슈카월드"]] = playlists["슈카"]
    filtermap[channels["슈카월드 코믹스"]] = playlists["슈카"]
    filtermap[channels["중괄호"]] = playlists["중괄호"]
    filtermap[channels["중괄호 다시보기"]] = playlists["중괄호"]


    filtermap[channels["알뷰"]] = TECHSHORT
    filtermap[channels[""]] = TECH

    filtermap[channels["안될공학 - IT 테크 신기술"]] = TECH
    filtermap[channels["Gadget Seoul"]] = TECH

    #filtermap[channels["테크기어캐스트 Tech Gear Cast"]] = REVIEW
    filtermap[channels["게임장비리뷰 겜용이"]] = REVIEW
    filtermap[channels["Luv IT ATO  러빗아토"]] = REVIEW
    filtermap[channels["JN테크리뷰"]] = REVIEW
    filtermap[channels["HB note"]] = REVIEW
    filtermap[channels["UNDERkg"]] = REVIEW
    filtermap[channels["집연구소 HomeLabs"]] = REVIEW
    filtermap[channels["뻘짓연구소"]] = REVIEW
    filtermap[channels["민티저"]] = REVIEW
    filtermap[channels["에이트 ATE"]] = REVIEW
    filtermap[channels["도레"]] = REVIEW
    filtermap[channels["ITSub잇섭"]] = REVIEW
    filtermap[channels["인싸IT"]] = REVIEW
    filtermap[channels["눈쟁이"]] = REVIEW
    filtermap[channels["신성조"]] = REVIEW
    filtermap[channels["말방구 실험실"]] = REVIEW
    filtermap[channels[""]] = REVIEW
    filtermap[channels[""]] = REVIEW

    filtermap[channels["코딩애플"]] = CODING
    filtermap[channels["노마드 코더 Nomad Coders"]] = CODING
    filtermap[channels["포프TV"]] = CODING
    filtermap[channels["GodotWorld"]] = CODING
    filtermap[channels["오늘코딩"]] = CODING
    filtermap[channels["HeartBeast"]] = CODING
    filtermap[channels["IBM Technology"]] = CODING
    filtermap[channels["Bramwell"]] = CODING
    filtermap[channels[""]] = CODING

    filtermap[channels["Cinecom.net"]] = CPUSTUDY
    filtermap[channels["C# Ui Academy"]] = CPUSTUDY
    filtermap[channels["Blender Guru"]] = CPUSTUDY
    filtermap[channels["Satya Achmad"]] = CPUSTUDY
    filtermap[channels["송캠프99"]] = CPUSTUDY
    filtermap[channels["Jie Jenn"]] = CPUSTUDY
    filtermap[channels["t3ssel8r"]] = CPUSTUDY
    filtermap[channels["ThioJoe"]] = CPUSTUDY
    filtermap[channels["Corey Schafer"]] = CPUSTUDY
    filtermap[channels[""]] = CPUSTUDY
    
    filtermap[channels["지식한입"]] = KNOW
    filtermap[channels["지식해적단"]] = KNOW
    filtermap[channels["너 진짜 똑똑하다"]] = KNOW
    filtermap[channels["길 인간학연구소"]] = KNOW
    filtermap[channels["한눈에 보는 세상 – Kurzgesagt"]] = KNOW
    filtermap[channels["Veritasium 한국어 - 베리타시움"]] = KNOW
    filtermap[channels["안될과학 Unrealscience"]] = KNOW
    filtermap[channels["동아시아유니버스"]] = KNOW
    filtermap[channels["놀면서 배우는 심리학"]] = KNOW
    filtermap[channels["스토리텔링 우동이즘 (이야기 작법)"]] = KNOW
    filtermap[channels[""]] = KNOW

    filtermap[channels["MBCNEWS"]] = NEWS
    filtermap[channels[""]] = NEWS


    filtermap[channels["에스텔잉글리쉬EstellEnglish"]] = ENG
    filtermap[channels[""]] = ENG

    filtermap[channels["설악산불다람쥐"]] = CLIP
    filtermap[channels[""]] = CLIP

    filtermap[channels["AsmrProg"]] = MUSIC
    filtermap[channels[""]] = MUSIC

    filtermap[channels["KBS COMEDY: 크큭티비"]] = TVREPLAY
    filtermap[channels["디글 클래식 :Diggle Classic"]] = TVREPLAY
    filtermap[channels["MIC SWG"]] = TVREPLAY
    filtermap[channels["KBS 한국방송"]] = TVREPLAY
    filtermap[channels["MBCentertainment"]] = TVREPLAY
    filtermap[channels[""]] = TVREPLAY


    filtermap[channels["OTR"]] = SHORT
    filtermap[channels["지식줄고양"]] = SHORT
    filtermap[channels[""]] = SHORT

    filtermap[channels["침착맨 플러스"]] = LONG
    filtermap[channels["긴도랜드"]] = LONG
    filtermap[channels["긴나성"]] = LONG
    filtermap[channels["Dr.Aquinas"]] = LONG
    filtermap[channels["중년게이머 긴실장"]] = LONG
    filtermap[channels["양아지 다시보기"]] = LONG
    filtermap[channels[""]] = LONG

    filtermap[channels["침착맨 원본 박물관"]] = LONGLONG
    filtermap[channels["똘똘똘이 다시보기"]] = LONGLONG

    filtermap[channels["여까네 유튜브"]] = MAIN
    filtermap[channels["똘똘똘이의 유튜브"]] = MAIN
    filtermap[channels["김도랜드"]] = MAIN
    filtermap[channels["중년게이머 김실장"]] = MAIN
    filtermap[channels["김나성"]] = MAIN
    filtermap[channels["the BOB studio | 더 밥 스튜디오"]] = MAIN
    filtermap[channels["셜록현준"]] = MAIN
    filtermap[channels["김성회의 G식백과"]] = MAIN
    filtermap[channels["호갱구조대"]] = MAIN
    filtermap[channels["취재대행소 왱"]] = MAIN
    filtermap[channels["채널 십오야"]] = MAIN
    filtermap[channels["너덜트"]] = MAIN
    filtermap[channels["주호민"]] = MAIN
    filtermap[channels["레바스튜디오"]] = MAIN
    filtermap[channels[""]] = MAIN
    
    filtermap[channels["ChuuChuuMeow"]] = SUB
    filtermap[channels["철면수심"]] = SUB
    filtermap[channels["승우아빠 일상채널"]] = SUB
    filtermap[channels["퀘이사존 QUASARZONE"]] = SUB
    filtermap[channels["김단군"]] = SUB
    filtermap[channels["우정잉"]] = SUB
    filtermap[channels["머독방송"]] = SUB
    filtermap[channels["오킹TV"]] = SUB
    filtermap[channels["김준표"]] = SUB
    filtermap[channels["면접왕 이형"]] = SUB
    filtermap[channels["SUNBA선바"]] = SUB
    filtermap[channels["승우아빠"]] = SUB
    filtermap[channels["미미미누"]] = SUB
    filtermap[channels["게임부록"]] = SUB
    filtermap[channels["탬탬버린"]] = SUB
    filtermap[channels["긱블 Geekble"]] = SUB
    filtermap[channels["충주시"]] = SUB
    filtermap[channels["스타크래프트"]] = SUB
    filtermap[channels["또모TOWMOO"]] = SUB
    filtermap[channels["전주MBC Original"]] = SUB
    filtermap[channels["Kamayana"]] = SUB
    filtermap[channels["장윤철[쭉튜브]"]] = SUB
    filtermap[channels[""]] = SUB
    filtermap[channels[""]] = SUB
    filtermap[channels[""]] = SUB

    filtermap["UC6JnCUR7MN9Okb86yVRx8Rg"] = SUB
    filtermap[""] = SUB

    filtermap[channels["혁펜하임"]] = UTIL
    filtermap[channels["오빠두엑셀 l 엑셀 강의 대표채널"]] = UTIL
    filtermap[channels["일잘러 장피엠"]] = UTIL
    filtermap[channels["마끼아또 Macciatto"]] = UTIL
    filtermap[channels["드림코딩"]] = UTIL
    filtermap[channels["임퓨의 비트메이킹 클래스"]] = UTIL
    filtermap[channels["3DGreenhorn"]] = UTIL
    filtermap[channels[""]] = UTIL


    filtermap[channels[""]] = CLIP
    filtermap[channels[""]] = CLIP

    filtermap[channels["클립애호가 Clip Devotee"]] = VTUBER
    filtermap[channels["홀로스터딩"]] = VTUBER
    filtermap[channels["버튜버 팬박스"]] = VTUBER
    filtermap[channels["허니츄러스 HoneyChurros"]] = VTUBER
    filtermap[channels["고등어 Ch."]] = VTUBER
    filtermap[channels["호소이누 Hosoinu"]] = VTUBER
    filtermap[channels["물색의별[Mulsec]"]] = VTUBER
    filtermap[channels["하타치 Hatachi"]] = VTUBER
    filtermap[channels["오리고기 ORIGOGI"]] = VTUBER
    filtermap[channels["manii 번역채널"]] = VTUBER
    filtermap[channels["Mr.10 / 홀로라이브 키리누키"]] = VTUBER
    filtermap[channels["서로Seo-Lo"]] = VTUBER
    filtermap[channels["야나기 Yanagi"]] = VTUBER
    filtermap[channels["V-Tuber 저장소"]] = VTUBER
    filtermap[channels["HOLO 번역하는 콘스프"]] = VTUBER
    filtermap[channels["하융 Haayung"]] = VTUBER
    filtermap[channels["BlackSheep까만양군"]] = VTUBER
    filtermap[channels["어르신 Ch. Oyakata"]] = VTUBER
    filtermap[channels["체리 Cherry"]] = VTUBER
    filtermap[channels["츠유 Tsuyu"]] = VTUBER
    filtermap[channels["홀로타입 HOLOTYPE"]] = VTUBER
    filtermap[channels["아메클립"]] = VTUBER
    filtermap[channels["쵸키 CHOKI [VRECORD]"]] = VTUBER
    filtermap[channels["홀로라이브 인도네시아 한글번역봇"]] = VTUBER
    filtermap[channels["빅타메"]] = VTUBER
    filtermap[channels["카에데클립 KaedeClip"]] = VTUBER
    filtermap[channels["요리사 클립"]] = VTUBER
    filtermap[channels["뮤매멈"]] = VTUBER
    filtermap[channels["시구레 원고방"]] = VTUBER
    filtermap[channels["버튜버 클립 연구소"]] = VTUBER
    filtermap[channels["시로쿠마 Shirokuma"]] = VTUBER
    filtermap[channels["해줘형 키리누커"]] = VTUBER
    filtermap[channels["타코사메펭귄"]] = VTUBER
    filtermap[channels["_alice cat"]] = VTUBER
    filtermap[channels["쓰나미 Tsunami"]] = VTUBER
    filtermap[channels["올리브 Ollieve"]] = VTUBER
    filtermap[channels["토끼굴 [rabbit hole]"]] = VTUBER
    filtermap[channels["카테고리8 Ch.08"]] = VTUBER
    filtermap[channels["타누키리누키 TanuKirinuki"]] = VTUBER
    filtermap[channels["샤이클립 Shyclip"]] = VTUBER
    filtermap[channels["브이레코드 VRECORD "]] = VTUBER
    filtermap[channels["시엘레"]] = VTUBER
    filtermap[channels["흔한키리누커 CommonKirinuker"]] = VTUBER
    filtermap[channels["moca"]] = VTUBER
    filtermap[channels["포항키츠네"]] = VTUBER
    filtermap[channels["감자 컴퓨터"]] = VTUBER
    filtermap[channels["김타기의 번역소"]] = VTUBER
    filtermap[channels["갸우르"]] = VTUBER
    filtermap[channels[""]] = VTUBER
    filtermap[channels[""]] = VTUBER


    filtermap["UCNJmYrylZ-VDXax94qAj36g"] = VTUBER # 라플라스最強伝説🛸💜
    filtermap["UCSde5FSvNqJgQlS_C4LK1JQ"] = VTUBER # 페코마리しか勝たん!
    filtermap["UC9uE0QLVycLb_UOg_ftmPeA"] = VTUBER # Morune Ch. モルネ
    filtermap["UCYVbNFh7KOpn7QHZAgiOWRg"] = VTUBER # 여우무침 / きつねどん
    filtermap["UC9F2tyKeE3Agm4t1e5-qTfw"] = VTUBER # 버추얼동물애호가
    filtermap["UCvfud8Iyi8-p9Kny2QXP7AA"] = VTUBER # 까치
    filtermap["UCqdf7eygBktV00E_Q_JD_ZA"] = VTUBER # 보노보노 Bonobono
    filtermap["UCZBKiVXBACk9WHvDcKx60yQ"] = VTUBER # Anthi7💎
    filtermap["UCyl370Da1skwvYpqo7HoUcw"] = VTUBER # 아큐라アキュラ
    filtermap["UCp5cDlDvsLUp6wjl4ELtmNw"] = VTUBER # 논리폭탄 LogicBomb
    filtermap["UCa8gOc8rmbYOe6lbsCr-sDA"] = VTUBER # (이름 없음)
    filtermap["UCyz8-nIRVAJGZ-1QrvnN46w"] = VTUBER # 로딩
    filtermap[""] = VTUBER # 
    
    
    
    filtermap[""] = ""
    
    filtermap.save()

if __name__ == "__main__":
    makeChannelFilterMap()