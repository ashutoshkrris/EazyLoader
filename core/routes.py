from core import app
from flask import render_template, send_file, request, session, flash, url_for, redirect
from pytube import YouTube
import pytube.exceptions as exceptions
from io import BytesIO


def convert_to_duration(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if hour > 0:
        return "%d:%02d:%02d" % (hour, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)


def convert_to_views(views):
    str_views = len(str(views))
    if str_views <= 3:
        return views
    elif str_views <= 6:
        return f"{round(views/1000,1)}K"
    elif str_views <= 9:
        return f"{round(views/1000000, 1)}M"
    else:
        return f"{round(views/1000000000,1)}B"


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
            duration = convert_to_duration(url.length)
            publish_date = url.publish_date.strftime("%b %d, %Y")
            return render_template('youtube/single/download.html', url=url, duration=duration, publish_date=publish_date, views=convert_to_views(url.views))
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
