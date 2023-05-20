from urllib.request import urlopen
import json
import pprint

def get_latest_commit():
    url = 'https://api.github.com/repos/himangshu147-git/ChickBot/commits?per_page=1'
    response = urlopen(url).read()
    data = json.loads(response.decode())
    return data[0]

pprint.pprint(get_latest_commit())