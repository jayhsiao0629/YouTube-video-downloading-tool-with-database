from flask import Blueprint, render_template, request, send_file
from pytube import YouTube
from .models import Video
from . import db
home = Blueprint("home", __name__)

@home.route("/", methods=["GET", "POST"])
def download_youtube_video():
    #訪問的時候是GET
    #送出表格時是POST
    if request.method == "POST":

        #把用戶在前端網頁輸入的網址取出來
        video_url = request.form.get("downloadUrl")
        
        #用取出來的網址 創一個新的youtube物件
        youtube_video_object = YouTube(video_url)

        #用這個物件裡面的功能 去取得影片的觀看數、作者還有影片名稱
        views = youtube_video_object.views
        author = youtube_video_object.author
        video_title = youtube_video_object.title

        #寫入資料庫
        new_video = Video(views, author, video_title)
        db.session.add(new_video)
        db.session.commit()

        #下載影片到伺服器
        get_video = youtube_video_object.streams.get_highest_resolution()

        #讓用戶端下載，選擇存放路徑
        return send_file(get_video.download(), as_attachment=True)
    #如果不是post 那他就是-> GET
    else:    
        #讀取資料庫
        videos = Video.query.all()
        return render_template("home.html", videos=videos)