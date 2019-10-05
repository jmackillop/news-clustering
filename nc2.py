#The plan
# 1 - Scrape headline links, and for each article, extract article content
# 2 - Named entity extraction
# 3 - Scikit-learn tf-idf vectorizer
# 4 - Clustering

import sys
import re
import spacy
import pandas as pd

# Step 1: Get links and contents
# Use approx top 10 or so from headline section on homepages of
# Guardian, NYT, BBC News, Reuters
# See get-article-texts.py for implementation
article_texts=[]
i=1
while True:
    try:
        f = open('article-text-%d' %i, 'r')
        article_texts.append(f.read())
        f.close()
        i+=1
    except:
        break



# Step 2: Named entity recognition
nlp = spacy.load("en_core_web_sm")
all_entities_listol = [] #list of lists
for t in article_texts:
    doc = nlp(t)
    article_entities = set()
    for ent in doc.ents:
        article_entities.add(ent.text)  
    all_entities_listol.append(article_entities)
# Note that there are often several entities that are effectively the same 
# e.g. Boris Johnson, the prime minister, Mr.Johnson




# Step 3: tf-idf vectorizer
# Aim to have, for each article, a vector of size = #(all named entities)
# Each element of the vector corresponds to the tf-idf value for a particular named entity

# Step 3a: Vocab and corpus
# Vocabulary is all the named entities
vocab = set()
for article_entities in all_entities_listol:
    for entity in article_entities:
        vocab.add(entity)
# Need vocab to be in dict form for CountVectorizer, with keys as terms and values as indices
vocab_dict={}
i=0
for ent in vocab:
    vocab_dict[ent]=i
    i+=1

# To develop the corpus, we use 10,000 recent reuters world news articles from the archives
# this is several months worth of articles
# See reuters-corpus.py for the implementation
f = open('reuters-corpus-10k-text.txt', 'r') #the corpus
docs = re.split(r'\n{4}',f.read()) #\n\n\n\n splits the articles in the corpus file f
docs = docs[:-1] #remove final empty string

# Step 3b: Compute idf values
# Use corpus to find the inverse document frequency(idf)

# First get counts in corpus of vocab words/phrases
from sklearn.feature_extraction.text import CountVectorizer
# Set vocab and limit to phrases of 1-4 tokens, then get document-term matrix
vectorizer = CountVectorizer(vocabulary=vocab_dict, ngram_range=(1,10))
word_count_vector = vectorizer.transform(docs)
# word_count_vector is a sparse matrix with (a row is a line in corpus) and (a column is a word in vocab)
# print(word_count_vector.shape) shows corpus is 10k articles, vocab ~1k phrases

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)
# to see idf values, put in data frame
# df_idf = pd.DataFrame(tfidf_transformer.idf_, index = vectorizer.get_feature_names(), columns = ['idf-weights'])
# df_idf = df_idf.sort_values(by=['idf-weights'])
# print(df_idf.head(10)) #shows idf weights of most common in the corpus of the ~1k 'vocab' 

# Step 3c: Compute tfidf values for each article
articles_word_count_vector = vectorizer.transform(article_texts[:2])
print(articles_word_count_vector)
tfidf_vector = tfidf_transformer.transform(articles_word_count_vector)

# first_article_vector = tfidf_vector[0]
# df = pd.DataFrame(first_article_vector.T.todense(), index = vectorizer.get_feature_names(), columns=['tfidf'])
# df = df.sort_values(by=['tfidf'], ascending=False)
# print(df.head(20))
# print(all_entities_listol[0])