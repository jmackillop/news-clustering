# news-clustering

My objective with this python program is to be able to identify the overall top news stories among the headlines of several of my favourite news publications, and then for each event/topic return a handful of articles from my favourite sites so I can get a different take on the top stories. So for example, if it is identified that a top story is a political debate from the previous night, I want to get a few articles on that from among my favourite publications.

The entire program is written in python, with help from a few libraries.

To start, I manually wrote the code for each news site to pull the top 10 or so news stories' urls from the headlines section. I tried to use the newspaper3k library for this (more later), but it was buggy for me (and others it seems). While this means the program isn't as easily scalable if I wanted to include many more news sites, this is fine for my personal purposes as I don't regularly look at any more than half a dozen or so news sources, so manually scraping is in this case (hopefully) a case of avoiding overengineering.

With the urls of the top 10 or so news headlines from each publication, I then used the newspaper3k library to extract the article text, which I then tidied up slightly by filtering out some leftover html as it seems to not pick up on certain formatting. (The newspaper3k library can do other things such as extracting the authors or the publication dates just as easily, but we leave things there for now).

The next step for the data preprocessing is to perform named entity recognition, which I did using SpaCy. The logic here is that news events are more or less uniquely identifiable by the people, places, companies, etc which are mentioned in them, and so if I can accurately identify the named entities for each article, then it becomes relatively easy, with a bit of machine learning, to cluster these articles into news events.

Once named entity recognition is performed, the next preprocessing step is to perform tf-idf vectorization of the named entities, and then perform clustering on the articles.
