import tweepy
import csv
import pandas as pd
import os
import itertools
import threading
import time
import sys

consumer_key = 'KEY'
consumer_secret = 'KEY SECRET'
access_token = 'TOKEN'
access_token_secret = 'TOKEN SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

candidates = ["Buttigieg"] ##"Klobuchar", "Buttigieg""Sanders", "Biden","Warren"
hashtags = ["Super+Tuesday"]#,"#SuperTuesday", "#SuperTuesday2020"
rt_tag = " -filter:retweets"

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done_scrapping:
            break
        sys.stdout.write('\r' + 'Extracting...' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!')

def scrappy(array):
    for c in array:
        print("Scrapping Twitter data for " + c + "...")
        file_counter = 0
        filename = c+"-after{}.csv"
        while os.path.isfile(filename.format(file_counter)):
            file_counter += 1
        filename = filename.format(file_counter)
        query = c + rt_tag
        tw_query(filename, query)
        time.sleep(60 * 3) # sleep for 3 minutes

def tw_query(filename, query):
    done_scrapping = False
    t.start() # animate loader
    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        tw_count = 0
        for tweet in tweepy.Cursor(api.search, q=query, lang="en").items():
            tw_count += 1
            if (not tweet.retweeted) and ('RT @' not in tweet.text):
               writer.writerow([tweet.created_at, tweet.text, tweet.user.location, tweet.coordinates])
    done_scrapping = True # finish loader
    print("\n\tFinished extracting and saving " + str(tw_count) + " tweets for " + c + ".")

done_scrapping = False
t = threading.Thread(target=animate)
t.daemon = True
scrappy(candidates)
#scrappy(hashtags)
t.join()
