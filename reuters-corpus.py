# To develop the corpus, we use 10,000 recent reuters world news articles from the archives
# this is several months worth of articles

import requests
import re
corpus_link_endings=[]
for i in range(100,1101):
    #Start from page 100 to exclude most recent articles
    # we dont want the ~50 chosen articles (or closely related) in the corpus
    rr = requests.get('https://uk.reuters.com/news/archive/worldnews?view=page&page='+str(i))
    links = re.findall(r'<a href="(/article/.+?)"', rr.text)
    for j in range(10): #to remove extraneous links (note 10 articles per page)
        corpus_link_endings.append(links[1+2*j])
corpus_links=[]
for end in corpus_link_endings:
    corpus_links.append('https://uk.reuters.com'+end)
# for link in corpus_links:
#     print(link,'\n')
f = open('reuters-corpus-10k-links.txt','w+')
for link in corpus_links:
    f.write(link+'\n')
f.close()

# # Extract contents of article from url using newspaper3k
# corpus_texts = []
# from newspaper import Article
# for link in corpus_links:
#     a = Article(link)
#     a.download()
#     a.parse()
#     corpus_texts.append(a.text)
# # i=0
# # for text in corpus_texts:
# #     print(text,i)
# #     i+=1

# # Write corpus-texts to a file
# f = open('reuters-corpus-10k.txt','w+')
# for text in corpus_texts:
#     f.write(text+'\n\n\n\n\n\n\n')
# f.close()