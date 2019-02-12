import nltk
import json
from nltk.corpus import stopwords
import string
# filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.OpenFileName("Open JSON File", filter)
# data = json.load('gg2013.json')


with open('gg2013.json') as f:
    data = json.load(f)


# possible function for finding number of hosts, may just want to track in main loop
def num_hosts():
    tweet_stream = ''
    for tweet in data:
        tweet_stream = tweet_stream + tweet["text"]


stop_words = (stopwords.words('english'))
stop_words.extend(['golden', 'globe', 'globes', 'goldenglobes', 'rt'])

hosts = []
i = 0
# could move lowercasing to entire text string but I think this will work better if we have to go tweet by tweet
for t in data:
    tweet = t["text"]
    if tweet[:2] != "RT":
        for ch in string.punctuation:
            tweet = tweet.replace(ch, "")

        tokens = [t.lower() for t in tweet.split() if t.lower() not in stop_words]
        host_terms = ['host', 'hosts', 'cohost', 'cohosts',
                      'co-host', 'hosting', 'co-hosts', 'coshosts']
        # need faster method, might take too long
        if any(t in host_terms for t in tokens):
            i = i + 1
            hosts.extend(nltk.bigrams(tokens))

freq = nltk.FreqDist(hosts)
# for key, val in freq.items():
#     if val > 100:
#         print (str(key) + ':' + str(val))

print(sorted(freq, key=freq.get, reverse=True)[:2])
print(i)
