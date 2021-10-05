from core import app
from flask import render_template, send_file, request, session, flash, url_for, redirect
from pytube import YouTube, Playlist
import pytube.exceptions as exceptions
from io import BytesIO


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
            last_updated = url.last_updated.strftime("%b %d, %Y")
            return render_template('youtube/playlist/download.html', url=url, last_updated=last_updated, views=convert_to_views(url.views))
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
        except Exception:
            flash('Unable to fetch the videos from YouTube Playlist')
            return redirect(url_for('yt_playlist_downloader'))

    return render_template('youtube/playlist/playlist.html')
