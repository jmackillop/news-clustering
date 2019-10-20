# Step 1: Scrape headline links
# Use approx top 10 or so from headline section on homepages of
# Guardian, NYT, BBC News, Reuters
import requests
import re
# The Guardian
rg = requests.get('https://www.theguardian.com/world')
all_g_links = re.findall(r'<h3.+href="(\S+)"', rg.text) #regular expression search
g_links = all_g_links[:10]
# NYTimes
rnyt = requests.get('https://www.nytimes.com')
nyt_link_endings = re.findall(r'e1aa0s8g0.*?href="(.*?html)', rnyt.text)
nyt_links = []
for ending in nyt_link_endings:
    nyt_links.append('https://www.nytimes.com'+ending)

# BBC News
rbbc = requests.get('https://www.bbc.co.uk/news/world')
bbc_link_endings = re.findall(r'href="(/news/[\w-]+[\d]+)"', rbbc.text) #r'href="(.*?)">\s::before', rbbc.text)
all_bbc_links = []
for end in bbc_link_endings:
    all_bbc_links.append('https://www.bbc.co.uk'+end)
bbc_links = [all_bbc_links[1]]+all_bbc_links[8:14]+all_bbc_links[20:23]

# Reuters
rr = requests.get('https://uk.reuters.com/news/world')
all_reuters_link_endings = re.findall(r'<a href="(/article/.+?)"', rr.text)
reuters_link_endings = []
for i in range(13):
    reuters_link_endings.append(all_reuters_link_endings[2*i])
reuters_links = []
for end in reuters_link_endings:
    reuters_links.append('https://uk.reuters.com'+end)


links = g_links+nyt_links+bbc_links+reuters_links




# Step 2: Extract article content
# Extract contents of article from url using newspaper3k
article_texts = []
from newspaper import Article
for link in links:
    a = Article(link)
    a.download()
    a.parse()
    article_texts.append(a.text)
# Save contents to files to improve run speeds while testing
i=1
for t in article_texts:
    f=open('article-text-%d' %i, 'w+')
    f.write(t)
    i+=1
    f.close()