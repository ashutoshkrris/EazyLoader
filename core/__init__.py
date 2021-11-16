from core.utils.momentjs import momentjs
from flask import Flask
from decouple import config
from core.utils.ig_downloader import IGDownloader
from logging.config import dictConfig
from core.utils.yt_downloader import YTDownloader
from flask_mail import Mail
from flask_socketio import SocketIO

IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
print("Logging into IG Account")
ig = IGDownloader(IG_USERNAME, IG_PASSWORD)
yt = YTDownloader()

mail = Mail(app)
socketio = SocketIO(app)


file_data = {}
status = {}

app.jinja_env.globals['momentjs'] = momentjs

from core.routes import core, instagram, youtube, slideshare, socket
from core.utils import custom_filters, playlist, contributors
