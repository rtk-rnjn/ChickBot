import requests
import random

def get_chick_fact():
    id = random.randint(1, 100)
    url = f"https://chickenfacts.io/api/v1/facts/{id}.json"
    response = requests.get(url)
    json = response.json()
    fact = json["fact"]
    return fact

