import requests
import os
import json
import urllib.parse

def run(query='cat'):
    url = f'https://twitter.com/search?q={query}'
    page = requests.get(url)
    for i in range(len(page.text)):
        if page.text[i:i+3] == 'wow':
            print(page.text[i:i+6])
run()
