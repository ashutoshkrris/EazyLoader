from core import app
from flask import render_template, send_file, request, session, flash, url_for, redirect
from pytube import YouTube, Playlist
import pytube.exceptions as exceptions
from io import BytesIO
from zipfile import ZipFile, ZipInfo

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import os
from pathlib import Path

from core.utils import playlist

chrome_options = Options()
chrome_options.headless = False

download_folder = str(os.path.join(Path.home(), "Downloads"))+'/'

name = datetime.now()
name = 'ig-video-' + name.strftime("%d-%m-%Y-%H:%M:%S")

@app.get('/')
def index():
    return render_template('index.html')


@app.route('/yt-downloader/video', methods=['GET', 'POST'])
def yt_video_downloader():
    if request.method == 'POST':
        session['video_link'] = request.form.get('video-url')
        try:
            url = YouTube(session['video_link'])
            url.check_availability()
            return render_template('youtube/single/download.html', url=url)
        except exceptions.MembersOnly:
            flash('Join this channel to get access to members-only content like this video, and other exclusive perks.')
            return redirect(url_for('yt_video_downloader'))
        except exceptions.RecordingUnavailable:
            flash('The video recording is not available!')
            return redirect(url_for('yt_video_downloader'))
        except exceptions.VideoPrivate:
            flash(
                'This is a private video. Please sign in to verify that you may see it.')
            return redirect(url_for('yt_video_downloader'))
        except Exception as e:
            print(e)
            flash('Unable to fetch the video from YouTube')
            return redirect(url_for('yt_video_downloader'))

    return render_template('youtube/single/video.html')


@app.post('/yt-downloader/video/download')
def download_video():
    buffer = BytesIO()
    url = YouTube(session['video_link'])
    itag = request.form.get("itag")
    video = url.streams.get_by_itag(itag)
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{url.title}.mp4", mimetype="video/mp4")


@app.route('/yt-downloader/playlist', methods=['GET', 'POST'])
def yt_playlist_downloader():
    if request.method == 'POST':
        session['playlist_link'] = request.form.get('playlist-url')
        try:
            url = Playlist(session['playlist_link'])
            return render_template('youtube/playlist/download.html', url=url)
        except exceptions.MembersOnly:
            flash('Join this channel to get access to members-only content like this video, and other exclusive perks.')
            return redirect(url_for('yt_playlist_downloader'))
        except exceptions.RecordingUnavailable:
            flash('The video recording is not available!')
            return redirect(url_for('yt_playlist_downloader'))
        except exceptions.VideoPrivate:
            flash(
                'This is a private video. Please sign in to verify that you may see it.')
            return redirect(url_for('yt_playlist_downloader'))
        except Exception as e:
            print(e)
            flash('Unable to fetch the videos from YouTube Playlist')
            return redirect(url_for('yt_playlist_downloader'))

    return render_template('youtube/playlist/playlist.html')


@app.post('/yt-downloader/playlist/download')
def download_playlist():

    url = Playlist(session['playlist_link'])
    for video in url.videos:
        video.streams.get_highest_resolution().download()

    return redirect(url_for('yt_playlist_downloader'))


@app.route('/yt-downloader/playlist/calculate', methods=['GET', 'POST'])
def calculate_playlist_duration():
    if request.method == 'POST':
        try:
            playlist_link = request.form.get('playlist-url')
            pl = Playlist(playlist_link)
            pl_obj = playlist.Playlist(playlist_link)
            duration = pl_obj.get_duration_of_playlist([1, 1.25, 1.5, 1.75, 2])
            return render_template('youtube/duration/playlist.html', playlist=pl, duration=duration, result=True)
        except Exception:
            flash('Unable to fetch the videos from YouTube Playlist')
            return redirect(url_for('calculate_playlist_duration'))

    return render_template('youtube/duration/playlist.html')

@app.route('/ig-downloader/video', methods=['GET', 'POST'])
def ig_video_downloader():
    if request.method == 'POST':
        try:
            driver = webdriver.Chrome(options=chrome_options)
            url = request.form['video-url']
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"_5wCQW")))

            soup = BeautifulSoup(driver.page_source, 'lxml')
            source = soup.find("video", class_="tWeCl")
            video = requests.get(source['src'],allow_redirects=True)
            
            if 'video' in (video.headers)['Content-type']:
                open(download_folder+name+'.mp4','wb').write(video.content)
            driver.quit()
        except Exception:
            flash('Unable to fetch and download the video, try again!','error')
            return redirect(url_for('ig_video_downloader'))
        
    return render_template('instagram/video.html')


