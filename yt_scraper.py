import googleapiclient.discovery 
import googleapiclient.errors
import os
from dotenv import load_dotenv
import pandas as pd

ty_vid = input("Input youtube video url: ")
vid_ID = ty_vid.split("=")[1]

api_service_name = "youtube"
api_version = "v3"

load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")


youtube = googleapiclient.discovery.build(
    api_service_name,api_version,developerKey=DEVELOPER_KEY
)

request = youtube.commentThreads().list(
    part = "snippet",
    videoId = vid_ID,
    order ="relevance",
    maxResults=200,
)

response = request.execute()

comments = []

for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']
    if comment['likeCount'] >= 0:
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['updatedAt'],
            comment['likeCount'],
            comment['textDisplay']
        ])

while response.get('nextPageToken', None):
    request = youtube.commentThreads().list(
    part = "snippet",
    videoId = vid_ID,
    order = "relevance",
    pageToken = response['nextPageToken'])
    response = request.execute()
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        if comment['likeCount'] >= 0:
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
        ])


df = pd.DataFrame(comments,columns=['author','published_at','updated_at','like_count','text'])

df.to_csv('/Users/joshliu/Desktop/side_projects/youtube_comment_sentiment/yt_vid_comments2.csv')