import sys
import re
import spacy
import pandas as pd
import numpy as np

# Step 1: Get links and contents
article_texts=[]
i=1
while True:
    try:
        f = open('article-text-%d' %i, 'r')
        article_texts.append(re.sub("’","'", f.read()))#fix apostrophes
        f.close()
        i+=1
    except:
        break



# Step 2: Named entity recognition
nlp = spacy.load("en_core_web_sm")
all_entities_listol = [] #list of lists
for t in article_texts:
    doc = nlp(t)
    article_entities = []
    for ent in doc.ents:
        if ent.text.lower() not in article_entities:
            article_entities.append(ent.text.lower())  
    all_entities_listol.append(sorted(article_entities))



# Step 3: tf-idf vectorizer
# Step 3a: Vocab and corpus
vocab = []
for article_entities in all_entities_listol:
    for entity in article_entities:
        if entity.lower() not in vocab:
            vocab.append(entity.lower()) #lowercase for CountVectorizer
vocab=sorted(vocab)
f = open('reuters-corpus-10k-text.txt', 'r')
docs = re.split(r'\n{4}',f.read()) #\n\n\n\n splits the articles in the corpus file f
docs = docs[:-1] #remove final empty string


# Step 3b: Compute idf values (using corpus)
# First get counts in corpus of vocab words/phrases
from sklearn.feature_extraction.text import CountVectorizer
cv1 = CountVectorizer(vocabulary=vocab, analyzer = 'word', ngram_range=(1,4))
corpus_vocab_count_matrix = cv1.transform(docs)
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(corpus_vocab_count_matrix)
# #to see idf values, put in data frame
# df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(), columns=['idf-weights'])
# df_idf = df_idf.sort_values(by=['idf-weights'])
# print(df_idf.head(10)) #shows idf weights of most common in the corpus of the ~1k 'vocab' 


# Step 3c: Compute tfidf values for each article
cv2 = CountVectorizer(vocabulary=vocab, analyzer = 'char', ngram_range=(1,30))
articles_vocab_count_matrix = cv2.transform([article_texts[0]])
#avcm = np.asarray(articles_vocab_count_matrix.todense())
tfidf_vector = tfidf_transformer.transform(articles_vocab_count_matrix)
ti = np.asarray(tfidf_vector.todense())
## See tfidf for first article
df = pd.DataFrame(ti[0], index=cv2.get_feature_names(), columns=['tfidf'])
df_descending = df.sort_values(by=['tfidf'], ascending=False)
#print(df_descending.head(5))

dfindices = [df.index[i] for i in range(len(vocab)) if df.iloc[i]['tfidf']>0]
print('tfidf!=0 but not in entity list', [w for w in dfindices if w not in all_entities_listol[0]])
print('in ent list but tfidf=0', [w for w in all_entities_listol[0] if w not in dfindices])
# these are in avcm, in tfidf_vector
print(len(all_entities_listol[0])) # =61

sys.exit()

'''Several entities in first article have tfidf of 0...not possible as they are in article'''
for entity in all_entities_listol[0][:5]:
    print(df.loc[entity,'tfidf'], entity)
