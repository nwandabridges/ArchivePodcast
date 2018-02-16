# Import dependencies
from bs4 import BeautifulSoup
import database
import datetime
import os
import requests
from tqdm import tqdm

shows = [
	'https://overcast.fm/itunes471418144/roderick-on-the-line',
	'https://overcast.fm/itunes1169249168/do-by-friday',
	'https://overcast.fm/itunes617416468/accidental-tech-podcast',
	'https://overcast.fm/itunes1001591287/reconcilable-differences',
	'https://overcast.fm/itunes415535037/back-to-work',
	'https://overcast.fm/itunes1030602911/road-work',
	'https://overcast.fm/itunes277928864/you-look-nice-today',
	'https://overcast.fm/p782999-cbxAGK'
	]

# Download entire show
def main(shows):
	database.main()
	for showURL in shows:
		show = getShowDetails(showURL)
		getEpisodeDetails(show)

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
		'overcastURL': showURL
		}

	# Write show to database
	connection = database.connect('podcasts.db')
	database.addRecord(connection, 'show', show)
	connection.close()

	show['page'] = showSoup

	return show

def getEpisodeDetails(show):
	# Get show details from database
	sql = "SELECT rowid FROM show WHERE overcastURL = '{}'".format(show['overcastURL'])
	connection = database.connect('podcasts.db')
	cursor = connection.cursor()
	cursor.execute(sql)
	rowid = cursor.fetchone()
	
	# Iterate through shows in page
	for record in tqdm(show['page'].find_all('a', {'extendedepisodecell usernewepisode'})):
		# Get episode details
		episode = {
			'show': rowid[0],
			'name': record.find('div', {'class': 'title singleline'}).string,
			'description': record.find('div', {'class': 'lighttext margintop05'}).string.strip(),
			'overcastURL': 'https://overcast.fm{}'.format(record['href'])
			}

		# Check if episode included in database
		sql = 'SELECT EXISTS(SELECT 1 FROM episode WHERE overcastURL="{0}" LIMIT 1);'.format(episode['overcastURL'])
		cursor = connection.cursor()
		cursor.execute(sql)
		included = cursor.fetchone()[0]

		if included == 0:
			# Load episode page
			episodePage = requests.get(episode['overcastURL'])
			episodeSoup = BeautifulSoup(episodePage.text, "lxml")
			
			# Add link to remote episode file and date
			episode['remoteFile'] = episodeSoup.source['src'].split('#')[0]
			episode['fileType'] = episode['remoteFile'].split('.')[-1]
			datestring = episodeSoup.find('div', {'class': 'margintop1'}).div.string.strip()
			episode['publishDate'] = str(datetime.datetime.strptime(datestring, '%B %d, %Y').date())

			# Download episode and save record to database
			episode['localFile'] = downloadEpisode(show, episode)
			database.addRecord(connection, 'episode', episode)

	connection.close()

def downloadEpisode(show, episode):
	# Create folder if folder doesn't exist
	if not os.path.exists(show['name']):
		os.makedirs(show['name'])

	# Download and store each episode
	file = requests.get(episode['remoteFile'])
	fileName = '{}/{} {}.{}'.format(show['name'], episode['publishDate'], episode['name'], episode['fileType'])
	with open(fileName, 'wb') as audio:
		audio.write(file.content)

	return fileName

if __name__ == '__main__':
	main(shows)