from pytube import YouTube
from io import BytesIO


class YTDownloader:
    """YouTube Downloader Class"""

    def download_single_video(self, video_link, itag):
        """Download single video from YouTube"""

        buffer = BytesIO()
        url = YouTube(video_link)
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer, url.title

    def download_audio(self, video_link):
        url = YouTube(video_link)
        audio = url.streams.get_audio_only()
        buffer = BytesIO()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer, url.title
