# Import dependencies
from bs4 import BeautifulSoup
import datetime
import os
import requests

showURL = 'https://overcast.fm/itunes617416468/accidental-tech-podcast'

def getShowDetails(showURL):
    # Download show feed
    showPage = requests.get(showURL)

    # Prepare show feed for parsing
    showSoup = BeautifulSoup(showPage.text, "lxml")

    # Get show details
    show = {
        'name': showSoup.find('h2', {'class': 'centertext'}).string,
        'link': showSoup.find('h2', {'class': 'margintop05 marginbottom0'}).a['href'],
        'description': showSoup.find('div', {'class':'margintop1 marginbottom1 lighttext'}).string.strip(),
        'overcastURL': showURL,
        'page': showSoup
        }
    return show

def getEpisodeDetails(show):
    # Create list to hold episodes
    episodes = []
    
    # Iterate through shows in page
    for record in show['page'].find_all('a', {'extendedepisodecell usernewepisode'}):
        # Get episode details
        episode = {
            'name': record.find('div', {'class': 'title singleline'}).string,
            'description': record.find('div', {'class': 'lighttext margintop05'}).string.strip(),
            'overcastURL': 'https://overcast.fm{}'.format(record['href'])
            }
        
        # Load episode page
        episodePage = requests.get(episode['overcastURL'])
        episodeSoup = BeautifulSoup(episodePage.text, "lxml")
        
        # Add link to remote episode file and date
        episode['remoteFile'] = episodeSoup.source['src'].split('#')[0]
        episode['fileType'] = episode['remoteFile'].split('.')[-1]
        datestring = episodeSoup.find('div', {'class': 'margintop1'}).div.string.strip()
        episode['publishDate'] = datetime.datetime.strptime(datestring, '%B %d, %Y').date()
        
        # Add episode to list of episodes
        episodes.append(episode)
    
    show['episodes'] = episodes
    
    return show

def downloadEpisodes(show):
    # Create folder if folder doesn't exist
    if not os.path.exists(show['name']):
        os.makedirs(show['name'])

    # Download and store each episode
    for episode in show['episodes']:
        file = requests.get(episode['remoteFile'])
        with open('{}/{} {}.{}'.format(show['name'], episode['publishDate'], episode['name'], episode['fileType']), 'wb') as audio:
            audio.write(file.content)

# Run processes
show = getShowDetails(showURL)
show = getEpisodeDetails(show)
downloadEpisodes(show)