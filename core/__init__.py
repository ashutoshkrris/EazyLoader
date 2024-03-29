from core.utils.momentjs import momentjs
from flask import Flask
from decouple import config
from core.utils.ig_downloader import IGDownloader
from core.utils.yt_downloader import YTDownloader
from core.utils.slideshare_downloader import SlideShareDownloader
from flask_mail import Mail
from flask_socketio import SocketIO

IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
try:
    print("Logging into IG Account")
    ig = IGDownloader(IG_USERNAME, IG_PASSWORD)
    @app.context_processor
    def inject_instagram():
        return dict(ig_working=True)
except Exception:
    print("Unable to login to IG account")
    ig = None
    @app.context_processor
    def inject_instagram():
        return dict(ig_working=False)
yt = YTDownloader()
ss = SlideShareDownloader()

mail = Mail(app)
socketio = SocketIO(app)


file_data = {}
status = {}

app.jinja_env.globals['momentjs'] = momentjs

from core.routes import core, instagram, youtube, slideshare, socket, pdf_tool
from core.utils import custom_filters, playlist, contributors
