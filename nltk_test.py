import nltk
import json
from nltk.corpus import stopwords
import string
# filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.OpenFileName("Open JSON File", filter)
# data = json.load('gg2013.json')

hosts = []
i = 0

with open('gg2013.json') as f:
    data = json.load(f)


stop_words = (stopwords.words('english'))
stop_words.extend(['golden', 'globe', 'globes', 'goldenglobes',
                   'year', 'next', 'made', 'performance', 'role', 'miniseries'])


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama',
                        'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy',
                        'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

condense_awards = ['cecil demille award',
                   'best motion picture drama',
                   'best performace actress drama',
                   'best performace actor drama',
                   'best motion picture comedy musical',
                   'actress comedy musical performance',
                   'actor comedy musical performace',
                   'animated feature film',
                   'foreign language film',
                   'supporting actress best',
                   'best supporting actor',
                   'best director',
                   'best screenplay',
                   'best score',
                   'best original song',
                   'best TV series',
                   'actress TV series',
                   'actor TV series',
                   'TV series comedy musical',
                   'actress TV mucial comedy',
                   'actor TV musical comedy',
                   'TV mini series picture',
                   'actress mini picture TV',
                   'actor mini picture TV',
                   'actress supporting TV series',
                   'actor supporting TV series']


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
                winner_name = " ".join(winner_name)
                if winner_name not in possible_winners:
                    possible_winners[winner_name] = 1
                else:
                    possible_winners[winner_name] += 1
        winners[award] = sorted(possible_winners, key=possible_winners.get, reverse=True)[: 1]
    # find tweets that contain certain percentage of award name,
    # remove stop words and award words,
    return winners


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters


host_tweets = []
award_tweets = []
presenter_tweets = []


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    host_terms = ['host', 'hosts', 'hosting', 'cohosts', 'cohosting', 'cohost']
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
            if any(w in host_terms for w in tokens):
                host_tweets.append(t)
            if "best" in tokens or "award" in tokens:
                award_tweets.append(t)

    print("Pre-ceremony processing complete.")
    return


def main():
    pre_ceremony()
    # print (get_hosts(host_tweets))
    # print (get_awards("2013"))
    winners = (get_winner("2013"))
    for keys, values in winners.items():
        print(keys)
        print(values)
    return


if __name__ == '__main__':
    main()


# ['tv', 'series', 'comedy', 'musical']
# ['actress', 'tv', 'mucial', 'comedy']
# ['actor', 'tv', 'musical', 'comedy']
# ['tv', 'mini', 'series', 'picture']
# ['actress', 'mini', 'picture', 'tv']
# ['actor', 'mini', 'picture', 'tv']
# ['actress', 'supporting', 'tv', 'series']
# ['actor', 'supporting', 'tv', 'series']
