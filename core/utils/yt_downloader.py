import os
from pytube import YouTube
from io import BytesIO


class YTDownloader:
    """YouTube Downloader Class"""

    def download_single_video(self, video_link, itag):
        """Download single video from YouTube"""

        url = YouTube(video_link)
        video = url.streams.get_by_itag(itag)
        # if int(itag) != url.streams.filter(res="1080p").first().itag:
        if True:
            buffer = BytesIO()
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            return buffer, video.default_filename

        # # If 1080p
        # vid = video.download()
        # os.rename(vid, "video.mp4")
        # audio = url.streams.get_audio_only()
        # aud = audio.download()
        # os.rename(aud, "audio.mp4")
        # os.system("ffmpeg -y -i video.mp4 -i audio.mp4 -c:v copy -c:a aac out.mp4 -loglevel quiet -stats")
        # os.remove("audio.mp4")
        # os.remove("video.mp4")
        # return os.path.abspath("out.mp4"), video.default_filename

    def download_audio(self, video_link):
        url = YouTube(video_link)
        audio = url.streams.get_audio_only()
        buffer = BytesIO()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer, url.title
