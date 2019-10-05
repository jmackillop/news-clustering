vocab = ['date', 'apple', 'banana', 'cherry']
vocab_dict={}
i=0
for ent in vocab:
    vocab_dict[ent]=i
    i+=1
fcorpus = open('test-corpus.txt', 'r')
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(vocabulary=vocab_dict, ngram_range=(1,2))
word_count_vector = vectorizer.transform(fcorpus)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)
print(tfidf_transformer.idf_)

# to check idf values, put in data frame
import pandas as pd
df_idf = pd.DataFrame(tfidf_transformer.idf_, index = vectorizer.get_feature_names(), columns=['idf-weights'])
df_idf = df_idf.sort_values(by=['idf-weights'])
print(df_idf)
