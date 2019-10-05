vocab = ['apple', 'banana', 'cherry']
vocab_dict={}
i=0
for ent in vocab:
    vocab_dict[ent]=i
    i+=1
fcorpus = open('test-corpus.txt', 'r')
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(vocabulary=vocab_dict, ngram_range=(1,2))
word_count_vector = vectorizer.transform(fcorpus)
print(word_count_vector.shape)
