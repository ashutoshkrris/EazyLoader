from core import app
from flask import render_template, send_file, request, flash, url_for, redirect, Response
from io import BytesIO
from decouple import config
import os
from core import ig
import shutil


IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')


@app.route('/ig-downloader/profile-pic', methods=['GET', 'POST'])
def ig_dp_downloader():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            if 'instagram.com' in username:
                flash('Please enter Instagram username, and not a link!', 'error')
                return redirect(url_for('ig_dp_downloader'))
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
            print(e)
            flash('Unable to fetch and download the profile picture, try again!', 'error')
            return redirect(url_for('ig_dp_downloader'))

    return render_template('instagram/profile_pic.html', title="Download Profile Picture")


@app.route('/ig-downloader/latest-stories', methods=['GET', 'POST'])
def ig_stories_downloader():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            if 'instagram.com' in username:
                flash('Please enter Instagram username, and not a link!', 'error')
                return redirect(url_for('ig_dp_downloader'))
            filename = ig.download_latest_stories(username)
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
        except Exception as e:
            print(e)
            flash('Unable to fetch and download the stories, try again!', 'error')
            return redirect(url_for('ig_stories_downloader'))

    return render_template('instagram/stories.html', title="Download Latest Stories")


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
            print(e)
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
            print(e)
            flash('Unable to fetch and download the video, try again!', 'error')
            return redirect(url_for('ig_video_downloader'))

    return render_template('instagram/video.html', title='Download Videos')
