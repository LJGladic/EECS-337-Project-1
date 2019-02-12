import nltk
import json
from nltk.corpus import stopwords
import string
# filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.OpenFileName("Open JSON File", filter)
# data = json.load('gg2013.json')

hosts = []
i = 0
award_dict = {}
with open('gg2013.json') as f:
    data = json.load(f)


# possible function for finding number of hosts, may just want to track in main loop
def num_hosts():
    tweet_stream = ''
    for tweet in data:
        tweet_stream = tweet_stream + tweet["text"]


# cut from less than 25 characterss
def awards_names(tokens):
    if "award" in tokens:
        if "best" in tokens:
            award = 'Best'
            for t in tokens[tokens.index("best") + 1:]:
                award += " "
                award += t
            award = "-".join(award.split("-", 2)[:2])
            return award
    return


stop_words = (stopwords.words('english'))
stop_words.extend(['golden', 'globe', 'globes', 'goldenglobes', 'rt', 'year', 'next'])

# could move lowercasing to entire text string but I think this will work better if we have to go tweet by tweet
for t in data:
    tweet = t["text"]
    if tweet[:2] != "RT":
        for ch in string.punctuation:
            #tweet = tweet.replace(ch, "")
            pass

        tokens = [t.lower() for t in tweet.split() if t.lower() not in stop_words]

        # for finding hosts
        # host_terms = ['host', 'hosts', 'cohost', 'cohosts',
        #               'co-host', 'hosting', 'co-hosts', 'coshosts']
        # # need faster method, might take too long
        # if any(t in host_terms for t in tokens):
        #     i = i + 1
        #     hosts.extend(nltk.bigrams(tokens))

        # for finding awards_names
        award_name = awards_names(tokens)
        if award_name is not None:
            if award_name not in award_dict:
                award_dict[award_name] = 1
            else:
                award_dict[award_name] += 1
freq = nltk.FreqDist(hosts)


print(sorted(freq, key=freq.get, reverse=True)[:2])
print(sorted(award_dict, key=award_dict.get, reverse=True)[:30])
print(i)


# change search for awards from best, to motion picture and television, then
# can get a seperate count for the amount of awards for each
