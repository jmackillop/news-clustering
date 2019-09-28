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
# for t in article_texts:
#     print(t,'\n\n\n\n\n')

# Step 2a: Named entity recognition
import spacy
nlp = spacy.load("en_core_web_sm")
all_entities_listol = [] #list of lists
for t in article_texts:
    doc = nlp(t)
    article_entities = set()
    for ent in doc.ents:
        article_entities.add(ent.text)  
    all_entities_listol.append(article_entities)
# print(all_entities_listol[10])
# Note that there is often several entities that are effectively the same 
# e.g. Boris Johnson, the prime minister, Mr.Johnson


# Step 2b: tf-idf vectorizer
# Aim to have, for each article, a size n vector where n = #(all named entities)
# Each element of the vector corresponds to the tf-idf value for a particular named entity

# Vocabulary is all the named entities
vocab = set()
for article_entities in all_entities_listol:
    for entity in article_entities:
        vocab.add(entity)
#Need vocab to be in dict form for CountVectorizer, with keys as terms and values as indices
vocab_dict={}
i=0
for ent in vocab:
    vocab_dict[ent]=i
    i+=1

# To develop the corpus, we use 10,000 recent reuters world news articles from the archives
# this is several months worth of articles
corpus_link_endings=[]
for i in range(100,1101):
    rr = requests.get('https://uk.reuters.com/news/archive/worldnews?view=page&page='+str(i))
    links = re.findall(r'<a href="(/article/.+?)"', rr.text)
    for j in range(10): #to remove extraneous links (note 10 articles per page)
        corpus_link_endings.append(links[1+2*j])
corpus_links=[]
for end in corpus_link_endings:
    corpus_links.append('https://uk.reuters.com'+end)
# Extract contents of article from url using newspaper3k
corpus_texts = []
from newspaper import Article
for link in corpus_links:
    a = Article(link)
    a.download()
    a.parse()
    corpus_texts.append(a.text)


from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(vocabulary=vocab_dict, ngram_range=(1,3)) #checks phrases with 1-3 tokens