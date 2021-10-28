import os
from instaloader import Instaloader, Post, Profile
from zipfile import ZipFile

class IGDownloader:
    """IGDownloader Class - takes login username and password as argument"""

    def __init__(self, login_username, login_password):
        self.loader = Instaloader()
        # self.loader.login(login_username, login_password)
        self.loader.post_metadata_txt_pattern = ''
        self.loader.save_metadata = False
        self.loader.download_comments = False

    def download_profile_picture(self, username: str) -> str:
        """Download profile picture for any Instagram profile

        Keyword arguments:
        username -- str
        Return: image filename
        """
        self.loader.download_pictures = True
        self.loader.download_videos = False

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
        self.loader.download_pictures = True
        self.loader.download_videos = False
    
        post_id = post_url.split('/')[4]
        try:
            post = Post.from_shortcode(self.loader.context, post_id)
            if post.is_video:
                return None

            if post.mediacount > 1:
                self.loader.download_post(post, post_id)
                zfname = f'{post_id}.zip'
                foo = ZipFile(zfname, 'w')
                # Adding files from directory 'post_id'
                for root, dirs, files in os.walk(f'{post_id}'):
                    for f in files:
                        if f.lower().endswith(('.png', 'jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
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

    def download_video(self, video_url) -> str or None:
        """Download post image from public accounts

        Keyword arguments:
        video_url -- str
        Return: video filename or None
        """

        self.loader.download_pictures = False
        self.loader.download_videos = True
        self.loader.post_metadata_txt_pattern = ''
        self.loader.save_metadata = False
        self.loader.download_comments = False

        video_id = video_url.split('/')[4]
        try:
            post = Post.from_shortcode(self.loader.context, video_id)
            if not post.is_video:
                return None

            self.loader.download_post(post, video_id)
            return video_id
        except Exception as e:
            print(e)
            return None

    def download_latest_stories(self, username: str):
        """Download post image from public accounts

        Keyword arguments:
        username -- str
        Return: zip filename or None
        """

        profile_id = self.loader.check_profile_id(username).userid
        try:
            self.loader.download_stories(userids=[profile_id], filename_target=username)
            
            zfname = f'{username}.zip'
            foo = ZipFile(zfname, 'w')
           # Adding files from directory 'post_id'
            for root, dirs, files in os.walk(username):
                for f in files:   
                    if not f.lower().startswith(('id')): 
                        foo.write(os.path.join(root, f))
                    os.remove(os.path.join(root, f))
            foo.close()
            os.removedirs(username)
            return zfname
        except Exception as e:
            print(e)
            return None
