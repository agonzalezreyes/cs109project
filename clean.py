import re, string
from bs4 import BeautifulSoup
import lxml

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "i'm", "it's", "", "don't", "&"]
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

at_thing = r'@[A-Za-z0-9]+'
url_thing = r'https?://[A-Za-z0-9./]+'
www = r'www\d{0,3}[.]\S+'
things = r'|'.join((at_thing, url_thing, www))

def remove_urls(txt):
    return re.sub('https?://[A-Za-z0-9./]+','', txt)

# removes links and caps letters
def clean_tweets(tweets):
    return [clean_a_tweet(tw) for tw in tweets]

# clean a single text entry
def clean_a_tweet(text):
    # decode html text
    sopa = BeautifulSoup(text, 'lxml')
    soupd = sopa.get_text()
    # remove urls and mentions
    strip_txt = re.sub(things, '', soupd)
    # handle utf-8 byte order mask
    try:
        remove_bom = strip_txt.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        remove_bom = strip_txt
    # clean hashtags, punctuation, and numbers
    letters_only = re.sub('[.,\-!?#$0-9]', '', remove_bom) #re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    no_extra_spaces = re.sub(' +', ' ', neg_handled)
    return no_extra_spaces

# @param text = sentence
def remove_stopwords(text):
    return " ".join([word for word in text.split() if word not in stop_words])

def create_bigrams(tweets):
    clean_tws = clean_tweets(tweets)
    tweets_no_stop_words = [remove_stopwords(tweet) for tweet in clean_tws]
    bigrams = [b for l in tweets_no_stop_words for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
    return bigrams

#tweets_no_urls = [remove_urls(tw) for tw in tweets]
#tweets_lowercase = [tw.lower() for tw in tweets_no_urls]
#re.sub(r"https:(\/\/t\.co\/([A-Za-z0-9]|[A-Za-z]){10})", "", txt)
# bigrams
# create lower case and split list of words for each tweet
#tweets_lowercase = [tweet.lower() for tweet in tweets]
# remove . at end of sentences
#tweets_no_punct = [re.sub('[.,\-!#$]', '', tw) for tw in tweets_lowercase]
# remove stop words from each tweet list of words
