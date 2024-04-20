from flask import Flask, send_file,render_template,request,session,redirect, url_for,flash
from io import BytesIO
from flask_session import Session
import re
import os
from flask import send_file
import io
import shutil
import instaloader
import ffmpeg
import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "Instagram Download"


@app.route("/")
def index():
    try:
        shutil.rmtree(os.path.join("/app/.git"))
        print(".git deleted")
    except:
        pass
    if not os.path.exists('/tmp/mukesh/'):
        os.makedirs('/tmp/mukesh/')
    clearEnv(os.path.join('/tmp/mukesh'))
    return render_template('index.html')
def clearEnv(path):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.mp4') or file.endswith('.mp3') or file.endswith('.jpg'):
            file_path = os.path.join(path, file)
            os.remove(file_path)

def valiDate(url,typrOfUrl):
    try:
        clearEnv(os.path.join('/tmp/mukesh'))
        if(typrOfUrl=='reels' or typrOfUrl=='reels_audio'):
            temp=url.split('reel')[1].split('/')[1]
            if(temp==''):
                return False
            return True
        elif(typrOfUrl=='post'):
            temp=url.split("/p")[1].split("/")[1]
            if(temp==''):
                return False
            return True
        elif(typrOfUrl=='dp'):
            temp=url.split(".com/")[1].split("?igsh")[0]
            if(temp==''):
                return False
            return True
        else:
            return False
        #return True
    except:
        return False

@app.route("/download", methods=["GET","POST"])
def download():
    session['Ig_url']=request.form["Ig_url"]
    session['ig_type']=request.form["ig_type"]
    print(session['Ig_url'],session['ig_type'])
    if(valiDate(session['Ig_url'],session['ig_type'])):
        L = instaloader.Instaloader()
        if(session['ig_type']=='reels'):
            print("url",session['Ig_url'])
            print("after split",session['Ig_url'].split('reel')[1].split('/')[1])
            post = instaloader.Post.from_shortcode(L.context, session['Ig_url'].split('reel')[1].split('/')[1])
            
            video_url = post.video_url
            filename = L.format_filename(post, target=post.shortcode)
            path=os.path.join('/tmp', 'mukesh/'+'Video_'+filename)
            L.download_pic(filename=path, url=video_url, mtime=post.date_utc)
            return send_file(str(path)+".mp4", as_attachment=True)
        elif(session['ig_type']=='reels_audio'):
            print("url",session['Ig_url'])
            print("after split",session['Ig_url'].split('reel')[1].split('/')[1])
            post = instaloader.Post.from_shortcode(L.context, session['Ig_url'].split('reel')[1].split('/')[1])
            
            video_url = post.video_url
            filename = L.format_filename(post, target=post.shortcode)
            path=os.path.join('/tmp', 'mukesh/'+'Video_'+filename)
            L.download_pic(filename=path, url=video_url, mtime=post.date_utc)
            try:
                input_stream = ffmpeg.input(path+".mp4")
                audio = input_stream.output(path+".mp3", format='mp3', acodec='libmp3lame')
                ffmpeg.run(audio, overwrite_output=True)
                return send_file(str(path)+".mp3", as_attachment=True)
            except Exception as e:
                flash("Dear user, please enter correct URL and select correct option", 'danger')
                return redirect(url_for('index'))
            #return send_file(str(path)+".mp4", as_attachment=True)
        elif(session['ig_type']=='post'):
            post_url = session['Ig_url'].split("/p")[1].split("/")[1]
            post = instaloader.Post.from_shortcode(L.context, post_url)
            photo_url = post.url
            video_url = post.video_url
            filename = L.format_filename(post, target=post.shortcode)
            print("filename",filename)
            path=os.path.join('/tmp', 'mukesh/'+'Video_'+filename)
            print("path",path)
            if(post.is_video):
                L.download_pic(filename=path, url=video_url, mtime=post.date_utc)
                return send_file(str(path)+".mp4", as_attachment=True)
            else:
                L.download_pic(filename=path, url=photo_url, mtime=post.date_utc)
                return send_file(str(path)+".jpg", as_attachment=True)
        elif(session['ig_type']=='dp'):
            username = session['Ig_url'].split(".com/")[1].split("?igsh")[0]
            profile = instaloader.Profile.from_username(L.context, username)
            profile_pic_url = profile.profile_pic_url
            path=os.path.join('/tmp', 'mukesh/'+username)
            L.download_pic(filename=path, url=profile_pic_url, mtime=datetime.datetime(2024, 4, 3, 10, 45, 31))
            return send_file(str(path)+".jpg", as_attachment=True)
    else:
        flash("Dear user, please enter correct URL and select correct option", 'danger')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route("/about")
def about():
    return "Developed BY Mukesh"

if __name__ == '__main__':
    app.run(debug=True)