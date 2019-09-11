#The plan
# 1 - Scrape headline links
# 2 - For each article, extract article content and then
#   2a - Named entity extraction
#   2b- Scikit-learn tf-idf vectorizer
# 3 - Clustering


# Step 1: get headline links
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


#  NOTE: NEWSPAPER3K IS BUGGY for .build, so had to use regex as above to pull in links

# Step 2: Article preprocessing
# Extract contents of article from url using newspaper3k
article_texts = []
from newspaper import Article
for link in links:
    quoted_link = "'"+link+"'"
    a = Article(link)
    a.download()
    a.parse()
    article_texts.append(a.text)
# Lots of \n\n in the article texts for new lines - we remove these here
for t in article_texts:
    line_of_text = re.findall(r'[^\n\n]+', t) #list of strings between each \n\n
    separator=' '
    t = separator.join(line_of_text) #for each article, change all instances of \n\n for a space

# Step 2a: Named entity recognition
import spacy
nlp = spacy.load("en_core_web_sm")
for a in article_texts:
    doc = nlp(a)
