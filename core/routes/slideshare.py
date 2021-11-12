from core import app, socketio, ss
from flask import render_template, send_file, request, session, flash, url_for, redirect
from flask_socketio import send
from threading import Thread
from time import sleep


file_data = {}
status = {}


@app.route('/slideshare-downloader/slides', methods=['GET', 'POST'])
def slide_downloader():
    if request.method == 'POST':
        session['slide_url'] = request.form.get('slide-url')
        try:
            title, image_url, total_slides, category, date, views = ss.get_slide_info(
                session['slide_url'])
            return render_template('slideshare/download.html', title=title, image_url=image_url, total_slides=total_slides, category=category, date=date, views=views)
        except Exception:
            flash('Please enter valid slideshare link', 'error')
            return redirect(url_for('slide_downloader'))
    return render_template('slideshare/slideshare.html', title="Download Slides")


def start_slide_preparation(msg, url):

    buffer, filename = ss.download_images(url)
    file_data.update(bfr=buffer)
    file_data.update(fname=filename)
    file_data.update(status="Done")
    status.update({f"{msg}": "Download-Ready"})


@socketio.on('message')
def socket_bidirct(msg):

    if msg[0] != "User has connected!":
        url = session['slide_url']
        t = Thread(target=start_slide_preparation, args=(
            msg[0], url,), daemon=True)
        t.start()

        while True:
            sleep(2)
            if status.get(msg[0]) == "Download-Ready":
                send("Download-Ready")
                break
        del status[msg[0]]

    if msg[0] == "User has connected!":
        print(msg[0])


@app.post('/slideshare-downloader/slides/download')
def download_slides():
    try:
        if file_data.get("status") == "Done":
            return send_file(file_data.get('bfr'), as_attachment=True, attachment_filename=file_data.get('fname'))
    except Exception:
        flash('Something went wrong while downloading', 'error')
        return redirect(url_for('slide_downloader'))
