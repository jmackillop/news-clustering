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
# Vocab is all the named entities
vocab = []
for article_entities in all_entities_listol:
    for entity in article_entities:
        if entity.lower() not in vocab:
            vocab.append(entity.lower()) #lowercase for CountVectorizer

# See reuters-corpus.py for the implementation of getting corpus
f = open('reuters-corpus-10k-text.txt', 'r')
docs = re.split(r'\n{4}',f.read()) #\n\n\n\n splits the articles in the corpus file f
docs = docs[:-1] #remove final empty string


# Step 3b: Compute idf values (using corpus)
# First get counts in corpus of vocab words/phrases
from sklearn.feature_extraction.text import CountVectorizer
# Set vocab and limit to phrases of 1-5 tokens, then get document-term matrix
cv = CountVectorizer(vocabulary=vocab, ngram_range=(1,5))
corpus_vocab_count_matrix = cv.transform(docs)
# N.B.: Vocab is ONLY named entities from original ~50 articles
# corpus_vocab_count_matrix is sparse matrix, row=(article in corpus) and column=(word in vocab)
# print(corpus_vocab_count_matrix.shape) shows corpus is 10k articles, vocab ~1k phrases
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(corpus_vocab_count_matrix)
# #to see idf values, put in data frame
# df_idf = (pd.DataFrame(tfidf_transformer.idf_, 
# index = cv.get_feature_names(), columns = ['idf-weights']))
# df_idf = df_idf.sort_values(by=['idf-weights'])
# print(df_idf.head(10)) #shows idf weights of most common in the corpus of the ~1k 'vocab' 


# Step 3c: Compute tfidf values for each article
articles_vocab_count_matrix = cv.transform(article_texts)
tfidf_vector = tfidf_transformer.transform(articles_vocab_count_matrix)

# # See tfidf for first article
# article_vector_1 = tfidf_vector[0]
# df = (pd.DataFrame(article_vector_1.T.todense(), index = cv.get_feature_names(), columns=['tfidf']))
# df = df.sort_values(by=['tfidf'], ascending=False)
# print(df.head(20))
# print(all_entities_listol[0])

print(tfidf_vector[0])
print(tfidf_vector.shape)
print(tfidf_vector.todense()[0])#tfidf values for vocabs from 0 to ~1k


'''TO DO: ?alphabetise vocab by sorting all_entities_listol?'''