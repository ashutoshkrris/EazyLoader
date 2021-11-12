from core import app, socketio
from flask import render_template, send_file, request, session, flash, url_for, redirect
from pytube import YouTube, Playlist
import pytube.exceptions as exceptions
from decouple import config
from core.utils import playlist
from core import yt
from flask_socketio import send
from threading import Thread
from time import sleep


file_data = {}
status = {}


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
            print(e)
            flash('Unable to fetch the video from YouTube', 'error')
            return redirect(url_for('yt_video_downloader'))

    return render_template('youtube/single/video.html', title='Download Video')


def start_preparation(msg, url, itag):

    buffer, filename = yt.download_single_video(url, itag)
    file_data.update(bfr=buffer)
    file_data.update(fname=filename)
    file_data.update(status="Done")
    status.update({f"{msg}": "Download-Ready"})


@socketio.on('message')
def socket_bidirct(msg):

    if msg[0] != "User has connected!":
        url = session['video_link']
        t = Thread(target=start_preparation, args=(
            msg[0], url, msg[1],), daemon=True)
        t.start()

        while True:
            sleep(2)
            if status.get(msg[0]) == "Download-Ready":
                send("Download-Ready")
                break
        del status[msg[0]]

    if msg[0] == "User has connected!":
        print(msg[0])


@app.post('/yt-downloader/video/download')
def download_video():
    try:
        if file_data.get("status") == "Done":
            return send_file(file_data.get('bfr'), as_attachment=True, attachment_filename=file_data.get('fname'), mimetype="video/mp4")
    except Exception:
        return redirect(url_for('yt_video_downloader'))


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
            print(e)
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
            print(e)
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
