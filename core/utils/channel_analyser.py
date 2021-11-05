from decouple import config
from googleapiclient.discovery import build


class ChannelAnalyser:
    def __init__(self, channel_username):
        self.youtube = build(
            'youtube', 'v3', developerKey=config("GOOGLE_CLIENT_API_KEY"))

        self.channel_username = channel_username
        self.channel = self.youtube.search().list(part='snippet', type='channel',
                                                  q=channel_username).execute()
        self.channel_id = self.channel['items'][0]['snippet']['channelId']

    def get_channel_stats(self):
        self.channel_info = self.youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()
        data = {
            "title": self.channel_info['items'][0]['snippet']['localized']['title'],
            "description": self.channel_info['items'][0]['snippet']['localized']['description'],
            'custom_url': self.channel_info['items'][0]['snippet']['customUrl'],
            'thumbnail_url': self.channel_info['items'][0]['snippet']['thumbnails']['default']['url'],
            'created_at': self.channel_info['items'][0]['snippet']['publishedAt'],
            "total_views": self.channel_info["items"][0]["statistics"]["viewCount"],
            "total_subscribers": self.channel_info["items"][0]["statistics"]["subscriberCount"],
            "total_videos": self.channel_info["items"][0]["statistics"]["videoCount"]
        }
        return data

    def get_all_playlists(self):
        playlists = []
        self.next_page_token = None
        while True:
            self.pl_request = self.youtube.playlists().list(
                part='snippet,contentDetails',
                channelId=self.channel_id,
                maxResults=50,
                pageToken=self.next_page_token
            )

            self.pl_response = self.pl_request.execute()

            self.playlist_items = self.pl_response['items']
            for item in self.playlist_items:
                playlists.append(
                    {
                        "id": item['id'],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"][:50],
                        "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
                        "playlist_url": f"https://www.youtube.com/playlist?list={item['id']}"
                    }
                )

            self.next_page_token = self.pl_response.get('nextPageToken')

            if not self.next_page_token:
                break

        return playlists

    def calculate_video_rating(self, likes, dislikes):
        total_reactions = int(likes)+int(dislikes)
        rating = round(((int(likes)/total_reactions)*100), 1)
        return rating

    def get_video_details(self, video_id):
        video = self.youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        video_details = {
            "uploaded_on": video["items"][0]["snippet"]["publishedAt"],
            "title": video["items"][0]["snippet"]["localized"]["title"],
            "id": video["items"][0]["id"],
            "statistics": {
                "total_views": video["items"][0]["statistics"]["viewCount"],
                "total_comments": video["items"][0]["statistics"]["commentCount"],
                "rating": self.calculate_video_rating(video["items"][0]["statistics"]["likeCount"], video["items"][0]["statistics"]["dislikeCount"])
            }
        }

        return video_details

    def get_latest_videos(self, num_of_videos):
        latest_videos = self.youtube.search().list(
            part='snippet',
            channelId=self.channel_id,
            maxResults=num_of_videos,
            order="date",
            type="video"
        ).execute()

        video_ids = []
        for video in latest_videos["items"]:
            video_ids.append(video["id"]["videoId"])

        latest_videos_details = []
        for id in video_ids:
            latest_videos_details.append(self.get_video_details(id))

        return latest_videos_details

    def get_most_viewed_videos(self, num_of_videos):
        latest_videos = self.youtube.search().list(
            part='snippet',
            channelId=self.channel_id,
            maxResults=num_of_videos,
            order="viewCount",
            type="video"
        ).execute()

        video_ids = []
        for video in latest_videos["items"]:
            video_ids.append(video["id"]["videoId"])

        latest_videos_details = []
        for id in video_ids:
            latest_videos_details.append(self.get_video_details(id))

        return latest_videos_details

    def get_highest_rated_videos(self, num_of_videos):
        latest_videos = self.youtube.search().list(
            part='snippet',
            channelId=self.channel_id,
            maxResults=num_of_videos,
            order="rating",
            type="video"
        ).execute()

        video_ids = []
        for video in latest_videos["items"]:
            video_ids.append(video["id"]["videoId"])

        latest_videos_details = []
        for id in video_ids:
            latest_videos_details.append(self.get_video_details(id))

        return latest_videos_details

    def get_most_relevant_videos(self, num_of_videos):
        latest_videos = self.youtube.search().list(
            part='snippet',
            channelId=self.channel_id,
            maxResults=num_of_videos,
            order="relevance",
            type="video"
        ).execute()

        video_ids = []
        for video in latest_videos["items"]:
            video_ids.append(video["id"]["videoId"])

        latest_videos_details = []
        for id in video_ids:
            latest_videos_details.append(self.get_video_details(id))

        return latest_videos_details
