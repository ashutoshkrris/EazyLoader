import requests


def fetch_posts():
    response = requests.get("https://iread.ga/api/v1/eazyloader/posts")
    return response.json()
