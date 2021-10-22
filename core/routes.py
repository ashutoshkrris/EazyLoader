from core import app
from flask import render_template, send_file, request, session, flash, url_for, redirect, Response
from pytube import YouTube, Playlist
import pytube.exceptions as exceptions
from io import BytesIO
from decouple import config
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from pathlib import Path
from selenium.webdriver.common.keys import Keys
import time
from core.utils import playlist
from core import ig

IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')

chrome_options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--incognito')

if not app.debug:
    GOOGLE_CHROME_PATH = config('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH = config('CHROMEDRIVER_PATH')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

download_folder = os.path.join(Path(__file__).resolve().parent.parent, "temp")


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
            flash('Join this channel to get access to members-only content like this video, and other exclusive perks.',
                  'error')
            return redirect(url_for('yt_video_downloader'))
        except exceptions.RecordingUnavailable:
            flash('The video recording is not available!', 'error')
            return redirect(url_for('yt_video_downloader'))
        except exceptions.VideoPrivate:
            flash(
                'This is a private video. Please sign in to verify that you may see it.')
            return redirect(url_for('yt_video_downloader'))
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch the video from YouTube', 'error')
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
            flash('Join this channel to get access to members-only content like this video, and other exclusive perks.',
                  'error')
            return redirect(url_for('yt_playlist_downloader'))
        except exceptions.RecordingUnavailable:
            flash('The video recording is not available!', 'error')
            return redirect(url_for('yt_playlist_downloader'))
        except exceptions.VideoPrivate:
            flash(
                'This is a private video. Please sign in to verify that you may see it.')
            return redirect(url_for('yt_playlist_downloader'), 'error')
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch the videos from YouTube Playlist', 'error')
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
            playlist_link = playlist_link.replace(
                "https://youtube", "https://www.youtube")
            playlist_link = playlist_link.replace(
                "https://m.youtube", "https://www.youtube")
            pl = Playlist(playlist_link)
            pl_obj = playlist.Playlist(playlist_link)
            duration = pl_obj.get_duration_of_playlist([1, 1.25, 1.5, 1.75, 2])
            return render_template('youtube/duration/playlist.html', playlist=pl, duration=duration, result=True)
        except Exception:
            flash('Unable to fetch the videos from YouTube Playlist', 'error')
            return redirect(url_for('calculate_playlist_duration'))

    return render_template('youtube/duration/playlist.html')


@app.route('/ig-downloader/video', methods=['GET', 'POST'])
def ig_video_downloader():
    if request.method == 'POST':

        try:
            if not app.debug:
                driver = webdriver.Chrome(
                    executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
            else:
                driver = webdriver.Chrome(options=chrome_options)
            url = request.form['video-url']
            driver.get(url)
            time.sleep(5)
            if 'Login' in driver.title:
                driver.find_element_by_name(
                    'username').send_keys(IG_USERNAME)
                time.sleep(2)
                password = driver.find_element_by_name(
                    'password')
                time.sleep(2)
                password.send_keys(IG_PASSWORD)
                password.send_keys(Keys.ENTER)

            open(os.path.join(download_folder, 'img.txt'),
                 'w').write(driver.get_screenshot_as_base64())
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_5wCQW")))
            soup = BeautifulSoup(driver.page_source, 'lxml')
            source = soup.find("video", class_="tWeCl")
            video = requests.get(source['src'], allow_redirects=True)

            if 'video' in (video.headers)['Content-type']:
                open(os.path.join(download_folder, 'ig-video.mp4'),
                     'wb').write(video.content)

            driver.quit()
            flash(
                f'Your video has been downloaded to {download_folder}!', 'success')
            return send_file(os.path.join(download_folder, 'ig-video.mp4'), as_attachment=True, mimetype="video/mp4")
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch and download the video, try again!', 'error')
            return redirect(url_for('ig_video_downloader'))

    return render_template('instagram/video.html')


@app.route('/ig-downloader/profile-pic', methods=['GET', 'POST'])
def ig_dp_downloader():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            filename = ig.download_profile_picture(username)
            file_path = os.path.join(os.path.abspath(username), filename)
            return_img = BytesIO()
            with open(file_path, 'rb') as fp:
                return_img.write(fp.read())
            return_img.seek(0)
            os.remove(file_path)
            os.removedirs(os.path.abspath(username))
            return send_file(return_img, mimetype='image/jpg', as_attachment=True, attachment_filename=f'{username}.jpg')
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch and download the profile picture, try again!', 'error')
            return redirect(url_for('ig_dp_downloader'))

    return render_template('instagram/profile_pic.html')


@app.route('/ig-downloader/image', methods=['GET', 'POST'])
def ig_image_downloader():
    if request.method == 'POST':
        try:
            post_url = request.form.get('post-url')
            post_url = post_url.replace(
                "https://instagram", "https://www.instagram")
            post_url = post_url.replace(
                "https://m.instagram", "https://www.instagram")
            filename = ig.download_image(post_url)
            if filename:
                if 'jpg' in filename:
                    return_img = BytesIO()
                    with open(filename, 'rb') as fp:
                        return_img.write(fp.read())
                    return_img.seek(0)
                    os.remove(filename)
                    return send_file(return_img, mimetype='image/jpg', as_attachment=True, attachment_filename=filename)
                elif 'zip' in filename:
                    with open(os.path.abspath(filename), 'rb') as fp:
                        data = fp.readlines()
                    os.remove(os.path.abspath(filename))
                    return Response(
                        data,
                        headers={
                            'Content-Type': 'application/zip',
                            'Content-Disposition': f'attachment; filename={filename}'
                        }
                    )
            else:
                flash(
                    'Please make sure the account is not private and the post contains image only!', 'error')
                return redirect(url_for('ig_image_downloader'))
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch and download the profile picture, try again!', 'error')
            return redirect(url_for('ig_image_downloader'))

    return render_template('instagram/picture.html')
