from decouple import config
import re
from datetime import timedelta
from googleapiclient.discovery import build


class PlaylistCalculator:
    def __init__(self, link_of_playlist):

        self.youtube = build(
            'youtube', 'v3', developerKey=config("GOOGLE_CLIENT_API_KEY"))

        self.hours_pattern = re.compile(r'(\d+)H')
        self.minutes_pattern = re.compile(r'(\d+)M')
        self.seconds_pattern = re.compile(r'(\d+)S')

        self.link_of_playlist = link_of_playlist

        self.total_seconds = 0
        self.total_videos = 0
        self.next_page_token = None

        self.playlist_id = ""
        self.pl_request = None
        self.pl_response = None

        self.vid_ids = None
        self.final_result = {}


    def get_duration_of_playlist(self, speeds):
        if self.link_of_playlist[0:4] == "http":
            if self.link_of_playlist[4] == 's':
                self.playlist_id = self.link_of_playlist[38::]
            else:
                self.playlist_id = self.link_of_playlist[37::]
        elif self.link_of_playlist[0:3] == "www":
            self.playlist_id = self.link_of_playlist[30::]
        else:
            return "Not a valid playlist URL"

        while True:
            self.pl_request = self.youtube.playlistItems().list(
                part="contentDetails",
                playlistId=self.playlist_id,
                maxResults=50,
                pageToken=self.next_page_token
            )

            self.pl_response = self.pl_request.execute()

            self.vid_ids = []
            for item in self.pl_response['items']:
                self.vid_ids.append(item['contentDetails']['videoId'])

            self.vid_request = self.youtube.videos().list(
                part="contentDetails",
                id=','.join(self.vid_ids)
            )

            self.vid_response = self.vid_request.execute()

            for item in self.vid_response['items']:
                duration = item['contentDetails']['duration']

                hours = self.hours_pattern.search(duration)
                minutes = self.minutes_pattern.search(duration)
                seconds = self.seconds_pattern.search(duration)

                hours = int(hours.group(1)) if hours else 0
                minutes = int(minutes.group(1)) if minutes else 0
                seconds = int(seconds.group(1)) if seconds else 0

                video_seconds = timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                ).total_seconds()

                self.total_seconds += video_seconds
            self.total_videos += len(self.vid_response['items'])

            self.next_page_token = self.pl_response.get('nextPageToken')

            if not self.next_page_token:
                break

        self.total_seconds = int(self.total_seconds)

        for speed in speeds:
            self.final_result[str(speed).replace(".","")] = self.convert_to_duration(
                self.total_seconds, speed)
            
        self.final_result["avg"] = self.convert_to_duration(self.total_seconds/self.total_videos, 1)

        return self.final_result

    def convert_to_duration(self, total_playlist_seconds, speed):
        total_seconds = total_playlist_seconds/speed
        self.days, total_seconds = divmod(total_seconds, 3600*24)
        self.hours, total_seconds = divmod(total_seconds, 3600)
        self.minutes, total_seconds = divmod(total_seconds, 60)

        if self.days > 0:
            return f"{int(self.days)} days, {int(self.hours)} hours, {int(self.minutes)} minutes, {int(total_seconds)} seconds"
        if self.hours > 0:
            return f"{int(self.hours)} hours, {int(self.minutes)} minutes, {int(total_seconds)} seconds"
        if self.minutes > 0:
            return f"{int(self.minutes)} minutes, {int(total_seconds)} seconds"
        if total_seconds > 0:
            return f"{int(total_seconds)} seconds"
