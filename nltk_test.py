import nltk
import json
from nltk.corpus import stopwords

# filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.OpenFileName("Open JSON File", filter)
# data = json.load('gg2013.json')


with open('gg2013.json') as f:
    data = json.load(f)

tweet_stream = ''
for tweet in data:
    tweet_stream = tweet_stream + tweet["text"]


tokens = [t for t in tweet_stream.split()]
freq = nltk.FreqDist(tokens)
for key, val in freq.items():

    print (str(key) + ':' + str(val))

# stopwords.words('english')
print(data[0]["text"])

# tokens = [t for t in data["text"].split()]
# freq = nltk.FreqDist(tokens)
