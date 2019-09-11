# news-clustering

My objective with this python program is to be able to identify the overall top news stories among the headlines of several of my favourite news publications, and then for each event/topic return a handful of articles from my favourite sites so I can get a different take on the top stories. So for example, if it is identified that a top story is a political debate from the previous night, I want to get a few articles on that from among my favourite publications.

The entire program is written in python, with help from a few libraries.

To start, I manually wrote the code for each news site to pull the top 10 or so news stories from the headlines section. I tried to use the newspaper3k library for this, but it was buggy for me (and others it seems). While this means the program isn't as easily scalable if I wanted to include many more news sites, this is fine for my personal purposes as I don't regularly look at any more than half a dozen or so news sources, so manually scraping is in this case (hopefully) a case of avoiding overengineering.

