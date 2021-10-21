import os
from instaloader import Instaloader, Post, Profile


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
