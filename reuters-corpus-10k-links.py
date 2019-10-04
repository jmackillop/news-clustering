# To develop the corpus, we use 10,000 recent reuters world news articles from the archives
# this is several months worth of articles
# This program gets the required links, from which the texts are found in reuters-corpus-10k-texts.py

import requests
import re
corpus_link_endings=[]
for i in range(100,1100):
    #Start from page 100 to exclude most recent articles
    # we dont want the ~50 chosen articles (or closely related) in the corpus
    rr = requests.get('https://uk.reuters.com/news/archive/worldnews?view=page&page='+str(i))
    links = re.findall(r'<a href="(/article/.+?)"', rr.text)
    for j in range(10): #to remove extraneous links (note 10 articles per page)
        corpus_link_endings.append(links[1+2*j])
    print(i) #to monitor progress (it takes a while)
corpus_links=[]
for end in corpus_link_endings:
    corpus_links.append('https://uk.reuters.com'+end)
# for link in corpus_links:
#     print(link,'\n')
f = open('reuters-corpus-10k-links.txt','w+')
for link in corpus_links:
    f.write(link+'\n')
f.close()