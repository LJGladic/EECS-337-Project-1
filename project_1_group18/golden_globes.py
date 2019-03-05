import nltk
import json
from nltk.corpus import stopwords
import string
import copy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from imdb import IMDb
from nltk.collocations import *
from nltk.metrics.association import QuadgramAssocMeasures
from requests import get
from bs4 import BeautifulSoup
# filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
# filename = rs.OpenFileName("Open JSON File", filter)
# data = json.load('gg2013.json')

i = 0
year = ""
db_year = ""
winners = []
movies = set()
people = set()
tv = set()

# with open('gg2013.json') as f:
#     data = json.load(f)


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
        hosts = []
        hosts.append(" ".join(sorted(freq, key=freq.get, reverse=True)[:2][0]))
        hosts.append(" ".join(sorted(freq, key=freq.get, reverse=True)[:2][1]))
        return hosts
    else:
        return " ".join(sorted(freq, key=freq.get, reverse=True)[:2][0])


def get_awards(year, winners):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''

    award_dict = {}
    for t in finding_award_tweets:
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
    winners_lst = []
    for keys, values in winners.items():
        winners_lst.append(values)
    awards_lst = sorted(award_dict, key=award_dict.get, reverse=True)[:32]
    final_awards_lst = []
    for award in awards_lst:
        if len(award) > 12:
            for winner in winners_lst:
                if winner in award:
                    final_awards_lst.append(award.replace(winner, ''))
    return final_awards_lst


def get_nominees(year, winners):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here

    if(year == "2013" or year == "2015"):
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819

    nominees = {}
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
        possible_nominees = {}
        human_name = False
        bgms = []
        winner = winners[award]
        winner_tokens = [t.lower() for t in winner.split()]
        if 'actor' in award_tokens or 'actress' in award_tokens or "director" in award_tokens:
            human_name = True

        for tweet in nominee_tweets:
            tweet_tokens = tweet["text"]
            combined_tokens = [value for value in award_tokens if value in tweet_tokens]
            percent = float(len(combined_tokens) / len(award_tokens))

            if percent > .8:
                nominee_name = [word for word in tweet_tokens if word not in award_tokens]
                if human_name:
                    bgms.extend(nltk.bigrams(nominee_name))
                else:
                    nominee_name = " ".join(nominee_name)
                    if nominee_name not in possible_nominees:
                        possible_nominees[nominee_name] = 1
                    else:
                        possible_nominees[nominee_name] += 1
        if human_name:
            freq = nltk.FreqDist(bgms)
            top_4 = []
            sorted_bgms = (sorted(freq, key=freq.get, reverse=True))
            x = 1
            while len(top_4) != 4:
                if x >= len(sorted_bgms):
                    break
                overlap = False
                for t in sorted_bgms[x]:
                    if(t in winner_tokens):
                        overlap = True

                if overlap == True:
                    x += 1
                    continue
                else:
                    name = " ".join(sorted_bgms[x])
                    if name in people:
                        top_4.append(name)
                        x += 1
                    else:
                        x += 1
                        continue
            nominees[award] = top_4
        else:
            top_4 = []
            x = 1
            possible_noms = sorted(possible_nominees, key=possible_nominees.get, reverse=True)
            while len(top_4) != 4:
                if x >= len(possible_noms):
                    break
                overlap = False
                nom_tokens = possible_noms[x].split()
                for t in nom_tokens:
                    if(t in winner_tokens):
                        overlap = True
                if overlap == True:
                    x += 1
                    continue
                else:
                    name = possible_noms[x]
                    if name in movies or name in tv:
                        top_4.append(possible_noms[x])
                        x += 1
                    else:
                        x += 1
                        continue
            nominees[award] = top_4
            #nominees[award] = sorted(possible_nominees, key=possible_nominees.get, reverse=True)[:4]

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
        # make sure that it doesn't mess it up
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
            winners[award] = " ".join(sorted(freq, key=freq.get, reverse=True)[:1][0])
        elif sorted(possible_winners, key=possible_winners.get, reverse=True)[0]:
            winners[award] = sorted(possible_winners, key=possible_winners.get, reverse=True)[0]
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

    possible_presenters = sorted(presenters_freq, key=presenters_freq.get, reverse=True)[:100]
    possible_presenters = [' '.join(person) for person in possible_presenters]
    possible_presenters = [person for person in possible_presenters if person in people]
    return possible_presenters


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
    # shortens award names
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
        for presenter in presenter_lst:
            if presenter in tweet:
                for award_name, award_tokens in short_award_names.items():
                    combined_tokens = [value for value in award_tokens if value in tweet_tokens]
                    percent = float(len(combined_tokens) / len(award_tokens))
                    if percent > .75:
                        if award_name not in presenters:
                            presenters[award_name] = [presenter]
                        else:
                            presenters[award_name].append(presenter)
                    else:
                        if award_name not in presenters:
                            presenters[award_name] = []

    for key, values in presenters.items():
        presenters[key] = values[:2]
        # print(values)
    return presenters


def get_red_carpet():
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
        if name.lower() in people:
            names[name] = 0
        # if ia.search_person(name):
        #     if ia.search_person(name)[0]['name'].lower() == name.lower():
        #         names[name] = 0

    for tweet in red_carpet_tweets:
        tokens = tweet["text"]
        text = " ".join(tokens)
        for n in names:
            if n in text:
                sentiment = analyzer.polarity_scores(text)
                names[n] += sentiment['compound']
    best = sorted(names, key=names.get, reverse=True)[:5]
    worst = sorted(names, key=names.get)[:5]
    return best, worst


def get_jokes():
    quadgram_measures = QuadgramAssocMeasures
    finder = QuadgramCollocationFinder.from_documents(joke_tweets)
    finder.apply_freq_filter(5)
    common = finder.nbest(quadgram_measures.pmi, 50)
    jokes = []
    for tweet in joke_original:
        for q in common:
            count = 0
            for word in q:
                if word in tweet:
                    count += 1
            if count == 4:
                add = True
                for j in jokes:
                    repeat = 0
                    for word in q:
                        if word in j:
                            repeat += 1
                    if repeat == 4:
                        add = False
                if add:
                    jokes.append(tweet)
                    common.remove(q)
    return jokes


host_tweets = []
award_tweets = []
finding_award_tweets = []
nominee_tweets = []
presenter_tweets = []
all_tweets = []
red_carpet_tweets = []
joke_tweets = []
joke_original = []


def movie_db(year):
    start = 1
    for page in range(1, 11):
        url = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&release_date=' \
              + year + '-01-01,' + year + '-12-31&sort=num_votes,desc&start=' + \
            str(start) + '&ref_=adv_nxt'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')
        for movie in movie_containers:
            name = movie.h3.a.text
            movies.add(name)
        start += 50
    return


def tv_db(year):
    start = 1
    for page in range(1, 11):
        url = 'https://www.imdb.com/search/title?title_type=tv_series,tv_miniseries&release_date=' \
              + year + '-01-01,' + year + '-12-31&sort=num_votes,desc&start=' + \
            str(start) + '&ref_=adv_nxt'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        tv_containers = html_soup.find_all('div', class_='lister-item mode-advanced')
        for title in tv_containers:
            name = title.h3.a.text
            tv.add(name)
        start += 50
    return


def person_db():
    start = 1
    for page in range(1, 31):
        url = 'https://www.imdb.com/search/name?gender=male,female&start=' + \
            str(start) + '&ref_=rlm'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        person_containers = html_soup.find_all('div', class_='lister-item mode-detail')
        for person in person_containers:
            name = person.h3.a.text
            # remove formatting
            name = name[1:-1].lower()
            people.add(name)
        start += 50
    return


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    host_terms = ['host', 'hosts', 'hosting', 'cohosts', 'cohosting', 'cohost']
    presenter_terms = ['presenting', 'presented', 'presenter', 'presents', 'present']
    try:
        with open('gg2013.json') as f:
            data = json.load(f)
    except:
        pass
    else:
        year = "2013"
        db_year = "2012"

    try:
        with open('gg2015.json') as f:
            data = json.load(f)
    except:
        pass
    else:
        year = "2015"
        db_year = "2014"

    try:
        with open('gg2018.json') as f:
            data = json.load(f)
    except:
        pass
    else:
        year = "2018"
        db_year = "2017"

    try:
        with open('gg2019.json') as f:
            data = json.load(f)
    except:
        pass
    else:
        year = "2019"
        db_year = "2018"

    # with open('gg2013.json') as f:
    #     data = json.load(f)
    for t in data:
        tweet = t["text"]
        if tweet[: 2] != "RT":
            for ch in string.punctuation:
                tweet = tweet.replace(ch, "")
            tokens = [t.lower() for t in tweet.split() if t.lower() not in stop_words]
            t["text"] = tokens
            all_tweets.append(t)
            if any(w in host_terms for w in tokens):
                host_tweets.append(t)
            if "best" in tokens or "award" in tokens:
                award_tweets.append(t)

            if "best" in tokens:
                finding_award_tweets.append(t)
            if "best" in tokens or "award" in tokens or "nominee" in tokens or "nominees" in tokens or "nominate" in tokens or "nominated" in tokens:
                nominee_tweets.append(t)
            if any(w in presenter_terms for w in tokens):
                presenter_tweets.append(t)
            if "red" in tokens and "carpet" in tokens:
                red_carpet_tweets.append(t)
            if "joke" in tokens:
                joke_tweets.append(t["text"])
                joke_original.append(tweet)
    person_db()
    movie_db(db_year)
    tv_db(db_year)
    print("Pre-ceremony processing complete.")
    return year, db_year


def main():
    year, db_year = pre_ceremony()

    if year == "2013" or year == "2015":
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819
    best, worst = get_red_carpet()
    hosts = (get_hosts(host_tweets))
    presenters = (get_presenters(year))
    winners = (get_winner(year))
    found_awards = (get_awards(year, winners))
    nominees = get_nominees(year, winners)
    jokes = get_jokes()
    json_output = {}
    json_output["hosts"] = hosts
    json_output["award_data"] = {}
    print(official_awards)
    for award_name in official_awards:
        award_name_no_punctuation = copy.deepcopy(award_name)
        for ch in string.punctuation:
            award_name_no_punctuation = award_name_no_punctuation.replace(ch, "")
        print(award_name)
        json_output["award_data"][award_name] = {}

        json_output["award_data"][award_name]["nominees"] = nominees[award_name_no_punctuation]
        json_output["award_data"][award_name]["presenters"] = presenters[award_name_no_punctuation]
        json_output["award_data"][award_name]["winner"] = winners[award_name_no_punctuation]

    with open('gg.json', 'w') as outfile:
        json.dump(json_output, outfile)

    n = len(hosts)
    for i in range(n):
        if i == n - 1:
            file.write(" ".join(hosts[i]).title())
        else:
            file.write(" ".join(hosts[i]).title() + ", ")
    file.write("\n")

    for award in official_awards:
        for ch in string.punctuation:
            award = award.replace(ch, "")
        file.write("Award: " + award)
        file.write("\n")

        file.write("Presenters: ")
        n = len(presenters[award])
        for i in range(n):
            if i == n - 1:
                file.write(presenters[award][i].title())
            else:
                file.write(presenters[award][i].title() + ", ")
        file.write("\n")

        file.write("Nominees: ")
        n = len(nominees[award])
        for i in range(n):
            if i == n - 1:
                file.write(nominees[award][i].title())
            else:
                file.write(nominees[award][i].title() + ", ")
        file.write("\n")

        file.write("Winner: " + winners[award].title())
        file.write("\n\n")

    file.write("(Our Found) Awards: \n")
    n = len(found_awards)
    for i in range(n):
        if i == n - 1:
            file.write(" ".join(found_awards[i]))
        else:
            file.write(" ".join(found_awards[i]) + ", ")
    file.write("\n\n")

    file.write("Best Dressed: ")
    n = len(best)
    for i in range(n):
        if i == n - 1:
            file.write(best[i].title())
        else:
            file.write(best[i].title() + ", ")
    file.write("\n")

    file.write("Worst Dressed: ")
    n = len(worst)
    for i in range(n):
        if i == n - 1:
            file.write(worst[i].title())
        else:
            file.write(worst[i].title() + ", ")
    file.write("\n\n")

    file.write("Best Jokes: \n")
    for joke in jokes:
        file.write(joke)
    file.write("\n")

    return


if __name__ == '__main__':
    main()
