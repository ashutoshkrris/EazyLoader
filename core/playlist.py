import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

class Playlist:
    def __init__(self, link_of_playlist):
        self.api_key = os.environ.get("Enter API KEY Here") # Need to replace "Enter API KEY here" with YT API's key while running the program
        
        self.hours_pattern = re.compile(r'(\d+)H')
        self.minutes_pattern = re.compile(r'(\d+)M')
        self.seconds_pattern = re.compile(r'(\d+)S')

        self.link_of_playlist = link_of_playlist

        self.total_seconds = 0
        self.next_page_token = None

        self.playlist_id = ""
        self.pl_request = None
        self.pl_response = None
        
        self.vid_ids = None


    def get_duration_of_playlist(self, speed):
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
            self.pl_request = self.youtube.playlistItems.list(
                part = "contentDetails",
                playlistId = self.playlist_id,
                maxResults = 50,
                pageToken = self.next_page_token
            )

            self.pl_response = self.pl_request.execute()

            self.vid_ids = []
            for item in self.pl_response['items']:
                self.vid_ids.append(item['contentDetails']['videoId'])

            self.vid_request = self.youtube.videos().list(
                part="contentDetails",
                id = ','.join(self.vid_ids)
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

            self.next_page_token = self.pl_response.get('nextPageToken')

            if not self.next_page_token:
                break

        self.total_seconds = int(self.total_seconds)

        self.total_seconds *= speed

        minutes, seconds = divmod(self.total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return(f'{hours}:{minutes}:{seconds}')

        


