# Extract contents of article from url using newspaper3k
# Links are from the program reuters-corpus-10k-links.py

# Get links from file
f = open('reuters-corpus-10k-links.txt','rU')
links = []
for line in f:
    links.append(line[:-1])# slice removes \n ending
f.close()

# Get text for each link
texts = []
from newspaper import Article
i=0
for link in links:
    a = Article(link)
    a.download()
    a.parse()
    texts.append(a.text)
    i+=1
    print('Downloaded link %d' %i)

# Write texts to a file
f = open('reuters-corpus-10k-text.txt','w+')
i=0
for text in texts:
    f.write(text+'\n\n\n\n')
    i+=1
    print('Written text %d' %i)
f.close()