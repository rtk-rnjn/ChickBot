import requests
import json

def thumbnail(identifier):
    r = requests.get(f"https://embed.spotify.com/oembed/?url=spotify:track:{identifier}")
    
    return r.json()["thumbnail_url"]