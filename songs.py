# songs.py
import random
from yt_dlp import YoutubeDL

def mood_songs_list(mood):
    try:
        ydl_opts = {'quiet': True, 'skip_download': True, 'format': 'bestaudio'}
        with YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch5:{mood} songs", download=False)['entries']
            if not search_result:
                return []

            # Return list of (title, url)
            return [(s['title'], s['webpage_url']) for s in search_result]

    except Exception as e:
        print("Error fetching songs:", e)
        return []