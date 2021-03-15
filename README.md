# YoutubeDownload

# 概要
Youtubeのチャンネルから動画をダウンロードするプログラムです。  
ダウンロードする動画は、動画時間指定・動画アップロード年月日の指定ができます。

![参考サイト1](https://www.sejuku.net/blog/70173)と![参考サイト2](https://qiita.com/g-k/items/7c98efe21257afac70e9)を参考にしました。

## 使用言語
言語はPythonです。



## Description


## Setting
以下のコマンドでYouTube APIを使えるようにします。
```bash
sudo pip3 install google-api-python-client
```
以下のコマンドでpytubeを使えるようにします。
```bash
sudo pip3 install pytube
```

## プログラムの編集箇所
### 10行目
Youtube Data APIの登録に関しては![参考サイト2](https://qiita.com/g-k/items/7c98efe21257afac70e9)を参考にしてください。
取得したAPIキーをプログラムにコピペしてください。  
### 11行目
ChannelIDはダウンロードしたいチャンネルのものを入力してください。  
ブラウザでチャンネルのページまで飛んで、URLにChannelIDが載っています。
