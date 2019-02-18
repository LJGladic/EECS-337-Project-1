import nltk
import json
from nltk.corpus import stopwords
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from imdb import IMDb
from collections import Counter
import re
# filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.OpenFileName("Open JSON File", filter)
# data = json.load('gg2013.json')

hosts = []
i = 0
with open('gg2013.json') as f:
    data = json.load(f)


stop_words = (stopwords.words('english'))
stop_words.extend(['golden', 'globe', 'globes', 'goldenglobes',
                   'year', 'next', 'made', 'performance', 'role', 'miniseries', 'video'])
stop_words.remove('will')


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama',
                        'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy',
                        'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


def get_hosts(tweets):
    cohost_terms = ['cohost', 'co-hosts', 'cohosts', 'cohosting']
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    hosts = []
    cohost_count = 1
    for t in tweets:
        tokens = t["text"]
        hosts.extend(nltk.bigrams(tokens))
        if any(w in cohost_terms for w in tokens):
            cohost_count += 1
    freq = nltk.FreqDist(hosts)
    if cohost_count > 10:
        return sorted(freq, key=freq.get, reverse=True)[:2]
    else:
        return sorted(freq, key=freq.get, reverse=True)[:1]


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''

    award_dict = {}
    awards = []
    for t in award_tweets:
        tokens = t["text"]
        award_name = 'best'
        for tok in tokens[tokens.index("best") + 1:]:
            award_name += " "
            award_name += tok

        if award_name is not None:
            if award_name not in award_dict:
                award_dict[award_name] = 1
            else:
                award_dict[award_name] += 1

        # remove tokens that are actors or movies
    return print(sorted(award_dict, key=award_dict.get, reverse=True)[:30])


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = {}
    if(year == "2013" or year == "2015"):
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819

    # punctuation fucked shit up
    for award in official_awards:
        for ch in string.punctuation:
            award = award.replace(ch, "")
        award_tokens = [t.lower() for t in award.split() if t.lower() not in stop_words]
        if 'television' in award_tokens:
            award_tokens[award_tokens.index('television')] = 'tv'

        if 'tv' in award_tokens:
            if 'motion' in award_tokens:
                award_tokens.remove('motion')
            if 'picture' in award_tokens:
                award_tokens.remove('picture')

        human_name = False
        bgms = []
        if 'actor' in award_tokens or 'actress' in award_tokens:
            human_name = True

        print (award_tokens)
        possible_winners = {}
        # check to see if tweet has words in award name
        # remove award words and stop words
        for tweet in award_tweets:
            tweet_tokens = tweet["text"]

            combined_tokens = [value for value in award_tokens if value in tweet_tokens]
            percent = float(len(combined_tokens) / len(award_tokens))
            #.7 with no punctuation
            if percent > .9:
                winner_name = [word for word in tweet_tokens if word not in award_tokens]
                if human_name:
                    bgms.extend(nltk.bigrams(winner_name))
                else:
                    winner_name = " ".join(winner_name)
                    if winner_name not in possible_winners:
                        possible_winners[winner_name] = 1
                    else:
                        possible_winners[winner_name] += 1
        if human_name:
            freq = nltk.FreqDist(bgms)
            winners[award] = " ".join(sorted(freq, key=freq.get, reverse=True)[
                                      :1][0])
        else:
            winners[award] = sorted(possible_winners, key=possible_winners.get, reverse=True)[:1]
    # find tweets that contain certain percentage of award name,
    # remove stop words and award words,
    return winners


def possible_presenters():
    # get list of possible presenters, search through tweets with extra stopwords unti we get a solid list
    possible_presenters = []
    presenter_terms = ['presenting', 'presented', 'presenter', 'present',
                       'presents', 'award', 'best', 'picture', 'motion', 'funny', 'president', 'amp', 'cecile', 'standing', 'ovation']
    for word in OFFICIAL_AWARDS_1315:
        presenter_terms.append(word)

    for tweet in presenter_tweets:
        tweet_tokens = tweet["text"]
        tweet_tokens = [word for word in tweet_tokens if word not in presenter_terms]
        possible_presenters.extend(nltk.bigrams(tweet_tokens))

    presenters_freq = nltk.FreqDist(possible_presenters)

    # print (len(presenters_freq))
    possible_presenters = sorted(presenters_freq, key=presenters_freq.get, reverse=True)[:50]
    # print(possible_presenters)
    possible_presenters2 = human_names(possible_presenters)
    #print ((possible_presenters2))
    # print (possible_presenters)
    return possible_presenters2


def human_names(names):
    ia = IMDb()
    tweet_names = []

    name_stop_words = []
    for name in names:
        new_name = " ".join(name)
        # if any(w in new_name for w in name_stop_words) is False:
        if ia.search_person(new_name):
            if new_name == ia.search_person(new_name)[0]['name'].lower():
                tweet_names.append(new_name)
                print(new_name)
    return tweet_names


# def get_presenters(year):
#     '''Presenters is a dictionary with the hard coded award
#     names as keys, and each entry a list of strings. Do NOT change the
#     name of this function or what it returns.'''
#     presenters = {}
#     if(year == "2013" or year == "2015"):
#         official_awards = OFFICIAL_AWARDS_1315
#     else:
#         official_awards = OFFICIAL_AWARDS_1819
#
#     award_time_dict = {}
#     # punctuation fucked shit up
#     for award in official_awards:
#         for ch in string.punctuation:
#             award = award.replace(ch, "")
#         award_tokens = [t.lower() for t in award.split() if t.lower() not in stop_words]
#         if 'television' in award_tokens:
#             award_tokens[award_tokens.index('television')] = 'tv'
#
#         if 'tv' in award_tokens:
#             if 'motion' in award_tokens:
#                 award_tokens.remove('motion')
#             if 'picture' in award_tokens:
#                 award_tokens.remove('picture')
#
#         # bgms = []
#
#         # check to see if tweet has words in award name
#         # remove award words and stop words
#         timestamp_counter = 0
#         timestamp_sum = 0
#         for tweet in award_tweets:
#             tweet_tokens = tweet["text"]
#
#             combined_tokens = [value for value in award_tokens if value in tweet_tokens]
#             percent = float(len(combined_tokens) / len(award_tokens))
#             if percent > .9:
#                 timestamp_counter += 1
#                 timestamp_sum += tweet["timestamp_ms"]
#                 # presenter_name = [word for word in tweet_tokens if word not in award_tokens]
#                 # bgms.extend(nltk.bigrams(presenter_name))
#
#         award_avg = float(timestamp_sum / timestamp_counter)
#         award_time_dict[award] = award_avg
#
#         # freq = nltk.FreqDist(bgms)
#         # presenters[award] = sorted(freq, key=freq.get, reverse=True)[:1]
#
# # list of names in presenter tweets, check to make sure that bigrams are bigrams in possible presenter
#     presenter_lst = possible_presenters()
#     print(presenter_lst)
#     for key, value in award_time_dict.items():
#         bgms = []
#         for tweet in all_tweets:
#             if value - 200000 < tweet["timestamp_ms"] < value:
#                 add_bigrams = [bgm for bgm in nltk.bigrams(tweet["text"]) if bgm in presenter_lst]
#                 bgms.extend(add_bigrams)
#         freq = nltk.FreqDist(bgms)
#         presenters[key] = sorted(freq, key=freq.get, reverse=True)[:5]
#     return presenters

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    presenters = {}
    if(year == "2013" or year == "2015"):
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819

    # holds shortened award names
    short_award_names = {}
    # keeps track of bigrams of tweets
    award_bigrams = {}
    for award in official_awards:
        for ch in string.punctuation:
            award = award.replace(ch, "")
        award_tokens = [t.lower() for t in award.split() if t.lower() not in stop_words]
        if 'television' in award_tokens:
            award_tokens[award_tokens.index('television')] = 'tv'

        if 'tv' in award_tokens:
            if 'motion' in award_tokens:
                award_tokens.remove('motion')
            if 'picture' in award_tokens:
                award_tokens.remove('picture')
        short_award_names[award] = award_tokens
        award_bigrams[award] = []

    # instead check if one of the names is in tweet, then check what award
    presenter_lst = possible_presenters()

    for tweet in award_tweets:
        tweet_tokens = tweet["text"]
        tweet = " ".join(tweet_tokens)
        tweet_bigrams = nltk.bigrams(tweet_tokens)
        # print('here')
        # print(presenter_lst)
        if any(presenter in tweet for presenter in presenter_lst):
            print("found award and presenter")
        if any(bgm in tweet_bigrams for bgm in presenter_lst):
            print("found bigram and presenter")
        for award_name, award_tokens in short_award_names.items():
            combined_tokens = [value for value in award_tokens if value in tweet_tokens]
            percent = float(len(combined_tokens) / len(award_tokens))
            if percent > .6:
                presenter_name = [word for word in tweet_tokens if word not in award_tokens]
                award_bigrams[award_name].extend(nltk.bigrams(presenter_name))

        # freq = nltk.FreqDist(bgms)
        # presenters[award] = sorted(freq, key=freq.get, reverse=True)[:1]

    # orders for each award

    for award_name, bigrams in award_bigrams.items():
        freq = nltk.FreqDist(bigrams)
        sorted_bgms = sorted(freq, key=freq.get, reverse=True)[:50]

        names = []
        for b in sorted_bgms:
            names.append(" ".join(b))
        #print (names)
        award_bigrams[award_name] = [name for name in names if name in presenter_lst]
        #print (award_name)
        # print(award_bigrams[award_name])

    # for tweet in all_tweets:
    #     add_bigrams = [bgm for bgm in nltk.bigrams(tweet["text"]) if bgm in presenter_lst]
    #     bgms.extend(add_bigrams)
    # freq = nltk.FreqDist(bgms)
    # presenters[key] = sorted(freq, key=freq.get, reverse=True)[:5]
    return presenters


def get_red_carpet(year):
    analyzer = SentimentIntensityAnalyzer()
    ia = IMDb()
    bgms = []
    names = {}

    for tweet in red_carpet_tweets:
        tokens = tweet["text"]
        try:
            tokens.remove("red")
            tokens.remove("carpet")
        except ValueError:
            pass
        bgms.extend(nltk.bigrams(tokens))
    freq = nltk.FreqDist(bgms)
    for bigram in sorted(freq, key=freq.get, reverse=True)[: 100]:
        name = " ".join(bigram)
        if ia.search_person(name):
            if ia.search_person(name)[0]['name'].lower() == name.lower():
                names[name] = 0

    for tweet in red_carpet_tweets:
        tokens = tweet["text"]
        text = " ".join(tokens)
        for n in names:
            if n in text:
                sentiment = analyzer.polarity_scores(text)
                names[n] += sentiment['compound']
    best = sorted(names, key=names.get, reverse=True)[: 5]
    worst = sorted(names, key=names.get)[: 5]
    print(best)
    print(worst)
    return


host_tweets = []
award_tweets = []
presenter_tweets = []
all_tweets = []
red_carpet_tweets = []


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    host_terms = ['host', 'hosts', 'hosting', 'cohosts', 'cohosting', 'cohost']
    presenter_terms = ['presenting', 'presented', 'presenter', 'presents', 'present']
    with open('gg2013.json') as f:
        data = json.load(f)
    for t in data:
        tweet = t["text"]
        if tweet[: 2] != "RT":
            for ch in string.punctuation:
                tweet = tweet.replace(ch, "")
            tokens = [t.lower() for t in tweet.split() if t.lower() not in stop_words]
            # print (tokens)
            t["text"] = tokens
            all_tweets.append(t)
            if any(w in host_terms for w in tokens):
                host_tweets.append(t)
            if "best" in tokens or "award" in tokens:
                award_tweets.append(t)
            if any(w in presenter_terms for w in tokens):
                presenter_tweets.append(t)
            if "red" in tokens and "carpet" in tokens:
                red_carpet_tweets.append(t)

    print("Pre-ceremony processing complete.")
    return


def main():
    pre_ceremony()
    # get_red_carpet("2013")
    hosts = (get_hosts(host_tweets))
    # print (get_awards("2013"))
    presenters = (get_presenters("2013"))
    for keys, values in presenters.items():
        print(keys)
        print(values)
    # winners = (get_winner("2013"))
    #nominees = get_nominees("2013")
    # for keys, values in winners.items():
    #     print(keys)
    #     print(values)
    # human_names('none')
    json_output = {}
    json_output["hosts"] = hosts
    json_output["award_data"] = {}
    for award_name in official_awards:
        json_output["award_data"][award_name] = {}
        json_output["award_data"][award_name]["nominees"] = nominees[award_name]
        json_output["award_data"][award_name]["presenters"] = presenters[award_name]
        json_output["award_data"][award_name]["winner"] = winners[award_name]

    with open('gg.json', 'w') as outfile:
        json.dump(data, outfile)
    return


if __name__ == '__main__':
    main()
