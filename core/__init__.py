from flask import Flask
from decouple import config
from core.utils.ig_downloader import IGDownloader

IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
print("Logging in")
ig = IGDownloader(IG_USERNAME, IG_PASSWORD)

from core import routes
from core.utils import custom_filters, playlist, contributors
