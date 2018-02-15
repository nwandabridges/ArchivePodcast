# ArchivePodcast

I created this script to download all of the episodes in the [Do By Friday After Show](https://www.patreon.com/dobyfriday). It worked well for that, but it doesn't generalize to other podcasts.  
  
I'd like this script to be a catch-all for downloading all episodes of any podcast.  
  
**Outstanding Problems:**
* RSS feeds are limited to a certain number of items, which means that feeds only contain the most recent *x* episodes. Rather than using RSS feeds, it may make sense to utilize a third-party catalogue like [Overcast](https://overcast.fm/itunes1169249168/do-by-friday).
* This script currently searches for .mp3 files, but podcasts are published in a variety of file types.
* Podcast metadata is *somewhat* standardized for iTunes. This script should take advantage of iTunes-like notation for retrieving episode/show metadata.