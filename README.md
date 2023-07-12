# Youtube Playlist Classifier

유투브 영상을 특정 기준에 맞게 분류해 원하는 재생목록으로 추가하는 파이썬 프로그램입니다

## 의존성

Python 3.10.6 을 기준으로 작성되었습니다

파이썬 패키지는 저장소 내 `dependency.sh`를 참조하세요

- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2
- oauth2client

이 프로그램을 사용하기 위해서는 구글의 Youtube API키와 OAuth 2.0 클라이언트 ID가 필요합니다

- [youtube-v3 시작하기](https://developers.google.com/youtube/v3/getting-started)
- [OAuth 2.0을 사용하여 Google API에 액세스하기 ](https://developers.google.com/identity/protocols/oauth2)

## 시작하기

1. OAuth 클라이언트 파일 `client_secret.json` 을 프로젝트 내 `auth\` 폴더 내에 추가합니다

2. 해당 포맷에 맞게 csv파일을 작성한 후 `.\app.py --set-filter [파일]` 을 실행해 필터를 등록합니다

| CHANNEL | CHANNEL_ID | PLAYLIST | PLAYLIST_ID | PLAYLIST_REDIRECT |
|---------|------------|----------|-------------|-------------------|
| `채널이름` | `채널 ID` | `재생목록 별명` | `재생목록 ID` | `리다이렉션 이름` |
| 채널 A | UCsJ61as... | 음악 | PLUE_U19ela... |  |
| 채널 B | UCsJ6dzx... | 짧은영상 | PLUE_U1zxvb... |  |
| 채널 C | UCsJ6dzx... | 음악 |  |  |
|  | | 짧 |  | 짧은영상 |

첫 행의 헤더를 정확하게 작성해야 오류가 나지 않습니다

**`CHANNEL`**
- csv 작성시 알아보기 편하기 위한 열로 프로그램 작동에 영향을 주지 않는 주석 영역입니다.

**`CHANNEL_ID`**
- 필터를 수행할 
- 채널ID 으로 프로그램의 READ 수행시 `data\channels.csv`에 title

**`PLAYLIST`**
- 재생목록의 별명을 나타냅니다.
- `CHANNEL_ID`와 같은 열에 있다면, 분류 수행시 `CHANNEL_ID`를 `PLAYLIST`가 가르키는 재생목록 ID로 분류하게 됩니다.

**`PLAYLIST_ID`**
- 재생목록 ID를 나타냅니다. 유튜브에서 재생목록을 들어갔을때 URL에서 _www.youtube.com/playlist?list=`재생목록ID`_ 부분을 복사해 가져올 수 있습니다.
- `PLAYLIST`와 같은 열에 있다면, `PLAYLIST`가 `PLAYLIST_ID` 을 가르키게 됩니다.
- `CHANNEL_ID`와 같은 열에 있다면, 분류 수행시 `CHANNEL_ID`를 `PLAYLIST_ID`가 가르키는 재생목록 ID로 분류하게 됩니다.

**`PLAYLIST_REDIRECT`**
- 같은 열 `PLAYLIST`가 비어있지 않아야 합니다.
- `PLAYLIST`가 `PLAYLIST_REDIRECT` 이름의 `PLAYLIST`가 가르키는 `PLAYLIST_ID`로 분류하도록 합니다.
- `PLAYLIST`, `PLAYLIST_ID`, `PLAYLIST_REDIRECT` 가 동시에 채워져있을 수 없습니다.

3. `./app.py` 를 실행해 명령줄 프로그램을 실행할 수 있습니다.

## 명령줄 옵션

| 옵션 | 설명 |
|------|-----|
| -a  | 인증 수행. `-r` `-c` 옵션 실행시 자동으로 수행됩니다. |
| -s `[재생목록ID]` | `[재생목록ID]`에서 동영상을 가져옵니다. `나중에 볼 영상` 은 가져올 수 없습니다. |
| -c  | `-s` 이용해 가져온 동영상을 필터를 이용해 분류를 수행합니다. |
| -i  | `-c` 로 분류된 동영상 정보를 각각의 재생목록에 추가합니다. |
| --verbose | verbose 모드. 더 많은 정보를 출력합니다 |
| --clear | `-c` 이용해 분류한 데이터를 청소합니다. |
| --get-channels `[파일]` | `-s` 통해 가져오는 과정에서 저장한 채널명, 채널ID 목록을 가져옵니다. |
|  --get-channels-noclassify `[파일]` | `--get-channels` 로 가져오는 채널중 목록에서 필터를 거쳤을 때, 분류되지 않은 채널만 가져옵니다. (`$LONG`, `$NOCLASSIFY`, `$SHORT`)는 분류되지 않은 것으로 취급합니다. |
| --get-filter `[파일]` | 현재 적용된 필터를 가져옵니다. |
| --set-filter `[파일]` | 새로운 필터를 적용합니다. |



*WIP*