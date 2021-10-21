import os
from instaloader import Instaloader, Post, Profile
import requests
from zipfile import ZipFile


class IGDownloader:
    """IGDownloader Class - takes login username and password as argument"""

    def __init__(self, login_username, login_password):
        self.loader = Instaloader()
        self.loader.login(login_username, login_password)

    def download_profile_picture(self, username: str) -> str:
        """Download profile picture for any Instagram profile

        Keyword arguments:
        username -- str
        Return: image filename
        """

        self.profile = Profile.from_username(self.loader.context, username)
        self.loader.download_profilepic(self.profile)
        img_file_name = os.listdir(username)[0]
        return img_file_name

    def download_image(self, post_url: str):
        """Download post image from public accounts

        Keyword arguments:
        post_url -- str
        Return: image filename or None
        """

        post_id = post_url.split('/')[4]
        try:
            post = Post.from_shortcode(self.loader.context, post_id)
            if post.is_video:
                return None
            if post.mediacount > 1:
                if not os.path.exists(post_id):
                    os.mkdir(post_id)
                li = list(post.get_sidecar_nodes())
                i = 1
                for l in li:
                    res = requests.get(l.display_url)
                    with open(f'{post_id}/{i}.jpg', 'wb') as f:
                        f.write(res.content)
                    i += 1
                zfname = f'{post_id}.zip'
                foo = ZipFile(zfname, 'w')
                # Adding files from directory 'post_id'
                for root, dirs, files in os.walk(f'{post_id}'):
                    for f in files:
                        foo.write(os.path.join(root, f))
                        os.remove(os.path.join(root, f))
                foo.close()
                os.removedirs(post_id)
                return zfname
            self.loader.download_pic(post_id, post.url, post.date_utc)
            return f'{post_id}.jpg'
        except Exception as e:
            print(e)
            return None
