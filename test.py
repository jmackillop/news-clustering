link = 'https://uk.reuters.com/article/uk-mideast-iran-tanker-britain/british-tanker-is-still-detained-in-iran-al-arabiya-tv-citing-british-foreign-ministry-idUKKBN1W81YE'
from newspaper import Article
a = Article(link)
a.download()
a.parse()
print(a.text)
print(link)