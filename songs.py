# songs.py
import random
#from youtubesearchpython import VideosSearch
#from pytube import Search
from yt_dlp import YoutubeDL

def mood_songs_list(mood, limit=5):
    """
    Returns a list of 5 songs (title + url) for a given mood.
    """
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'bestaudio',
        }
        with YoutubeDL(ydl_opts) as ydl:
            # Search for 10 songs matching the mood
            search_result = ydl.extract_info(f"ytsearch10:{mood} songs", download=False)['entries'] #entries is a list of search results

            if not search_result:
                return []

            # Pick 5 random songs (or less if fewer available)
            songs = random.sample(search_result, min(limit, len(search_result))) #random.sample picks unique items from the list, so we won't get duplicates. If there are fewer than 5 songs, it will return all of them.

            # Return list of tuples (title, url)
            return [(song['title'], song['webpage_url']) for song in songs]

    except Exception as e:
        print("Error fetching songs:", e)
        return []