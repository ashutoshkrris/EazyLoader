from flask import Flask
from decouple import config
from core.utils.ig_downloader import IGDownloader
from logging.config import dictConfig
from core.utils.yt_downloader import YTDownloader

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })


IG_USERNAME = config('IG_USERNAME', default='username')
IG_PASSWORD = config('IG_PASSWORD', default='password')

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
print("Logging into IG Account")
ig = IGDownloader(IG_USERNAME, IG_PASSWORD)
yt = YTDownloader()

from core import routes
from core.utils import custom_filters, playlist, contributors
