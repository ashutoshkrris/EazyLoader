from core import app
from flask import render_template, send_file, request, flash, url_for, redirect, Response
import os


@app.route("/pdf-tools/encrypt", methods=["GET", "POST"])
def encrypt_pdf_page():
    return render_template('pdf-tools/encrypt.html', title="Encrypt PDF")


@app.route("/pdf-tools/decrypt", methods=["GET", "POST"])
def decrypt_pdf_page():
    return render_template('pdf-tools/decrypt.html', title="Decrypt PDF")
