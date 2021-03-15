from apiclient.discovery import build
from apiclient.errors import HttpError
from pytube import YouTube

"""
----------------
---個人設定変数---
----------------
"""
API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'   #取得したAPIキーを入力(個人で違う)
CHANNEL_ID = 'xxxxxxxxxxxxxxxxxxxxxxxx'              #ダウンロードしたいチャンネルのIDを入力
DURATION_CRITERIA_HOUR = 2     #ダウンロードする動画の長さを指定　1の場合１時間未満の動画をダウンロード
DOWNDOAD_Tag = 22              #タグを指定 22か18を指定(動画によって違うので注意)
YEAR_Ceiling = 2100            #ダウンロードする動画の投稿日時を指定
MONTH_Ceiling = 12
YEAR_Floor = 2020
MONTH_Floor = 1
"""
以下４行のように期間指定すると、2100年１2月から2019年8月までの動画をダウンロード
YEAR_Ceiling = 2100
MONTH_Ceiling = 12
YEAR_Floor = 2020
MONTH_Floor = 1
"""


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
channels = [] #チャンネル情報を格納する配列
searches = [] #videoidを格納する配列
videos = [] #各動画情報を格納する配列
nextPagetoken = None
nextpagetoken = None


youtube = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

channel_response = youtube.channels().list(
    part = 'snippet,statistics',
    id = CHANNEL_ID
    ).execute()
    
#動画の長さを取得し、設定した長さかどうかを判断
def durationDetermine(duration):
    hour = 0
    minite = 0
    second = 0
    if duration[3] == 'H':
        hour = int(duration[2:3])
    elif duration[3] == 'M':
        minite = int(duration[2:3])
    elif duration[3] == 'S':
        second = int(duration[2:3])
    elif duration[4] == 'H':
        hour = int(duration[2:4])
    elif duration[4] == 'M':
        minite = int(duration[2:4])
    elif duration[4] == 'S':
        second = int(duration[2:4])
    if hour < DURATION_CRITERIA_HOUR:
        return True
    else:
        return False
    
#動画をダウンロード
def download(url, filename, date, duration):
    print(duration)
    if durationDetermine(duration):
        video = YouTube(url)
        print(filename + ' をダウンロード中')
        stream = video.streams.get_by_itag(DOWNDOAD_Tag)
        stream.download('./downloadMovie', date + filename)

#設定した期限内にアップされた動画かを判定
def uploadDateCheck(date):
    year = int(date[0:4])
    month = int(date[5:7])
    if YEAR_Floor <= year and year <= YEAR_Ceiling:
        if MONTH_Floor <= month or year > YEAR_Floor:
            if month <= MONTH_Ceiling or year < YEAR_Ceiling:
                return True
    return False


for channel_result in channel_response.get("items", []):
    if channel_result["kind"] == "youtube#channel":
        channels.append([channel_result["snippet"]["title"],channel_result["statistics"]["subscriberCount"],channel_result["statistics"]["videoCount"],channel_result["snippet"]["publishedAt"]])

while True:
    if nextPagetoken != None:
        nextpagetoken = nextPagetoken

    search_response = youtube.search().list(
      part = "snippet",
      channelId = CHANNEL_ID,
      maxResults = 50,
      order = "date", #日付順にソート
      pageToken = nextpagetoken #再帰的に指定
      ).execute()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            searches.append(search_result["id"]["videoId"])

    try:
        nextPagetoken =  search_response["nextPageToken"]
    except:
        break


for result in searches:
    video_response = youtube.videos().list(
      part = 'snippet,statistics,contentDetails',
      id = result
      ).execute()

    for video_result in video_response.get("items", []):
        if video_result["kind"] == "youtube#video":
            videos.append([video_result["snippet"]["title"],video_result["statistics"]["viewCount"],video_result["statistics"]["likeCount"],video_result["statistics"]["dislikeCount"],video_result["statistics"]["commentCount"],video_result["snippet"]["publishedAt"],video_result["id"]])  
        #ダウンロードする処理
        if uploadDateCheck(video_result["snippet"]["publishedAt"]):
            download('https://www.youtube.com/watch?v=' + result, video_result["snippet"]["title"], video_result["snippet"]["publishedAt"], video_result["contentDetails"]["duration"])