import os
import time
import requests
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_video_ids(songs):
    videoIds = []
    type = "video"
    part = "snippet"

    for song in songs:
        url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&q={song}&type={type}&part={part}"
        json_res = requests.get(url)
        res = json.loads(json_res.text)
        videoId = res["items"][0]["id"]["videoId"]
        videoIds.append(videoId)
    return videoIds
