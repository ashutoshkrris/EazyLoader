import requests


def fetch_posts():
    response = requests.get("https://ireadblog.com/api/v1/eazyloader/posts")
    return response.json()


def get_blog_post(id, slug):
    response = requests.get(f"https://ireadblog.com/api/v1/post/{id}/{slug}")
    return response.json()[0]
