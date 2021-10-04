from core import app
from flask import render_template, send_file


@app.get('/')
def index():
    return render_template('index.html')
