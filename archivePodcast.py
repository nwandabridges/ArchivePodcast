# Import dependencies
from bs4 import BeautifulSoup
from datetime import datetime
import requests

# Download show feed
page = requests.get('PUT SHOW URL HERE')

# Prepare show feed for parsing
soup = BeautifulSoup(page.text, "lxml")

# Get name of show
show = {
    'name': soup.find('itunes:name').string
}

print(str(datetime.now()) + ': Starting to download episodes of ' + show['name'])

# Get each episode from feed
for item in soup.find_all('item'):
    episode = {
        'title': item.title.string,
        'description': item.description.string,
        'pubDate': datetime.strptime(item.pubdate.string, '%a, %d %b %Y %H:%M:%S %Z'),
        'url': item.enclosure.get('url'),
        'file': requests.get(item.enclosure.get('url')).content
    }
    
    print(str(datetime.now()) + ': Currently downloading episode ' + episode['title'])
    
    with open(episode['title'] + '.mp3', 'wb') as audio:
        audio.write(episode['file'])