# ArchivePodcast

![](assets/22053587422_f0294533df_k.jpg?raw=true)  

Use this script to download and catalog all episodes of a podcast.
  
## Usage
1. Clone this repo to your local machine/server to use the script.  

2. Once you've downloaded the scripts, go to [Overcast](https://overcast.fm) and use the search box to find the podcast(s) that you'd like to archive.  

3. Replace lines 10-16 in [archivePodcast.py](archivePodcast.py) with the podcast URL(s) from Overcast and save the file.

4. Run [archivePodcast.py](archivePodcast.py).  

## Common Problems
- This script was written and tested with Python v3.6. It will not work with Python 2.
- This script utilizes several common external dependencies:
	- BeautifulSoup (for parsing html) `pip install beautifulsoup4`
	- Requests (for downloading webpages and content) `pip install requests`
	- lxml (for parsing web html) `pip install lxml`