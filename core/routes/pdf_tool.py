from core import app
from flask import render_template, request, flash, send_from_directory, redirect
import os
from werkzeug.utils import secure_filename
from core.utils.pdf_tools import decrypt_file, encrypt_file

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/pdf-tools/encrypt", methods=["GET", "POST"])
def encrypt_pdf_page():
    if request.method == "POST":
        if not 'pdf-file' in request.files:
            flash('PDF file is missing', 'error')
            return redirect(request.url)
        pdf_file = request.files['pdf-file']
        password = request.form.get('password')
        if password and len(password) < 5:
            flash('Password is too short, please choose a strong password', 'error')
            return redirect(request.url)

        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = saved_path.removesuffix('.pdf') + '_encrypted.pdf'
            output_name = filename.removesuffix('.pdf') + '_encrypted.pdf'
            pdf_file.save(saved_path)
            result = encrypt_file(saved_path, password, output_path)
            if result == 1:
                return send_from_directory(app.config['UPLOAD_FOLDER'], output_name, as_attachment=True)
            elif result == 2:
                flash(
                    'Your file is already encrypted. Feel free to decrypt it using our tool', 'error')
                return redirect(request.url)
            elif result == 3:
                flash('Error while reading your file', 'error')
                return redirect(request.url)

    return render_template('pdf-tools/encrypt.html', title="Encrypt PDF")


@app.route("/pdf-tools/decrypt", methods=["GET", "POST"])
def decrypt_pdf_page():
    if request.method == "POST":
        if not 'pdf-file' in request.files:
            flash('PDF file is missing', 'error')
            return redirect(request.url)
        if not 'password' in request.form:
            flash('Password is missing', 'error')
            return redirect(request.url)
        pdf_file = request.files['pdf-file']
        password = request.form.get('password')

        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = saved_path.removesuffix('.pdf') + '_decrypted.pdf'
            output_name = filename.removesuffix('.pdf') + '_decrypted.pdf'
            pdf_file.save(saved_path)
            result = decrypt_file(saved_path, password, output_path)
            if result == 1:
                return send_from_directory(app.config['UPLOAD_FOLDER'], output_name, as_attachment=True)
            elif result == 2:
                flash(
                    'Your file is already decrypted. Feel free to encrypt it using our tool', 'error')
                return redirect(request.url)
            elif result == 3:
                flash('Error while reading your file, please check your password', 'error')
                return redirect(request.url)
    return render_template('pdf-tools/decrypt.html', title="Decrypt PDF")
