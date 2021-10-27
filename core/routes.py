from core import app, mail
from flask import render_template, send_file, request, session, flash, url_for, redirect, Response
from pytube import YouTube, Playlist
import pytube.exceptions as exceptions
from io import BytesIO
from decouple import config
import os
from core.utils import playlist
from core import ig, yt
import shutil
from flask_mail import Message

IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')
ADMIN_EMAIL = config('ADMIN_EMAIL', default=None) 

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':    
        if True:
            name = request.form.get('name')
            email = request.form.get('email')
            ph_no = request.form.get('ph_no')
            message = request.form.get('message')
            
            msg = Message("HELLO", sender=ADMIN_EMAIL, recipients=[ADMIN_EMAIL])
            msg.html = "Hey, sending this email from my Flask app"
            mail.send(msg)
            return 'Mail sent!'
            
        # except Exception as e:
        #     return(str(e))

    return render_template('index.html', title='Home')


@app.route('/yt-downloader/video', methods=['GET', 'POST'])
def yt_video_downloader():
    if request.method == 'POST':
        session['video_link'] = request.form.get('video-url')
        try:
            highest_res = False
            url = YouTube(session['video_link'])
            url.check_availability()
            if url.streams.filter(res="1080p"):
                highest_res = url.streams.filter(res="1080p").first()
            return render_template('youtube/single/download.html', url=url, highest_res=highest_res)
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

    return render_template('youtube/single/video.html', title='Download Video')


@app.post('/yt-downloader/video/download')
def download_video():
    url = session['video_link']
    itag = request.form.get("itag")
    print(itag)
    buffer, filename = yt.download_single_video(url, itag)
    return send_file(buffer, as_attachment=True, attachment_filename=filename,mimetype="video/mp4")


@app.route('/yt-downloader/audio', methods=['GET', 'POST'])
def yt_audio_downloader():
    if request.method == 'POST':
        session['video_link'] = request.form.get('video-url')
        try:
            url = YouTube(session['video_link'])
            url.check_availability()
            return render_template('youtube/audio/download.html', url=url)
        except exceptions.MembersOnly:
            flash('Join this channel to get access to members-only content like this audio, and other exclusive perks.',
                  'error')
            return redirect(url_for('yt_audio_downloader'))
        except exceptions.RecordingUnavailable:
            flash('The audio recording is not available!', 'error')
            return redirect(url_for('yt_audio_downloader'))
        except exceptions.VideoPrivate:
            flash(
                'This is a private video and hence cannot get the audio. Please sign in to verify that you may see it.')
            return redirect(url_for('yt_audio_downloader'))
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch the video/audio from YouTube', 'error')
            return redirect(url_for('yt_audio_downloader'))

    return render_template('youtube/audio/audio.html', title='Download Audio')


@app.post('/yt-downloader/audio/download')
def download_audio():
    url = session['video_link']
    buffer, filename = yt.download_audio(url)
    return send_file(buffer, as_attachment=True, attachment_filename=f"{filename}.mp3", mimetype="audio/mp3")


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

    return render_template('youtube/playlist/playlist.html', title='Download YouTube Playlist')


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
            pl_obj = playlist.PlaylistCalculator(playlist_link)
            duration = pl_obj.get_duration_of_playlist([1, 1.25, 1.5, 1.75, 2])
            return render_template('youtube/duration/playlist.html', playlist=pl, duration=duration, result=True, title='Calculate Playlist Duration')
        except Exception:
            flash('Unable to fetch the videos from YouTube Playlist', 'error')
            return redirect(url_for('calculate_playlist_duration'))

    return render_template('youtube/duration/playlist.html', title='Calculate Playlist Duration')


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

    return render_template('instagram/profile_pic.html', title="Download Profile Picture")


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

    return render_template('instagram/picture.html', title='Download Images')


@app.route('/ig-downloader/video', methods=['GET', 'POST'])
def ig_video_downloader():
    if request.method == 'POST':
        try:
            video_url = request.form.get('video-url')
            video_url = video_url.replace(
                "https://instagram", "https://www.instagram")
            video_url = video_url.replace(
                "https://m.instagram", "https://www.instagram")
            folder_name = ig.download_video(video_url)

            # Delete after sending

            for (dirpath, dirnames, filenames) in os.walk(os.path.abspath(folder_name)):
                if not 'temp' in filenames[0]:
                    return_video = BytesIO()
                    with open(os.path.join(os.path.abspath(folder_name), filenames[0]), 'rb') as fp:
                        return_video.write(fp.read())
                    return_video.seek(0)
                    shutil.rmtree(os.path.abspath(folder_name))
                    return send_file(return_video, as_attachment=True, attachment_filename=f'{folder_name}.mp4')
        except Exception as e:
            app.logger.error(e)
            flash('Unable to fetch and download the video, try again!', 'error')
            return redirect(url_for('ig_video_downloader'))

    return render_template('instagram/video.html', title='Download Videos')


@app.route("/tos")
def tos():
    return render_template('tos.html', title='Terms of Service')


@app.route("/blog")
def blog():
    return render_template('blog.html', title='Blogs')


@app.route("/donate")
def donate():
    return render_template('donate.html', title='Make your donation now')


