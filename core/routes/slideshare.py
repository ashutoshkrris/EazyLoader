from core import app, ss, file_data, status
from flask import render_template, send_file, request, session, flash, url_for, redirect



@app.route('/slideshare-downloader/slides', methods=['GET', 'POST'])
def slide_downloader():
    if request.method == 'POST':
        session['slide_url'] = request.form.get('slide-url')
        ss.download_format = request.form.get('format')
        ss.slideshare_url = request.form.get('slide-url')

        try:
            title, image_url, total_slides, category, date, views = ss.get_slide_info()
            return render_template('slideshare/download.html', title=title, image_url=image_url, total_slides=total_slides, category=category, date=date, views=views)
        except Exception:
            flash('Please enter valid slideshare link', 'error')
            return redirect(url_for('slide_downloader'))
    return render_template('slideshare/slideshare.html', title="Download Slides")


def start_slide_preparation(msg, url):

    buffer, filename = ss.download_images()
    file_data.update(slide_bfr=buffer)
    file_data.update(slide_fname=filename)
    file_data.update(slide_status="Done")
    status.update({f"slide_{msg}": "Download-Ready"})


@app.post('/slideshare-downloader/slides/download')
def download_slides():
    try:
        if file_data.get("slide_status") == "Done":
            return send_file(file_data.get('slide_bfr'), as_attachment=True, attachment_filename=file_data.get('slide_fname'))
    except Exception:
        flash('Something went wrong while downloading', 'error')
        return redirect(url_for('slide_downloader'))
