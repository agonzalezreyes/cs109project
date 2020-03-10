import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
import re
# local files
import clean
training_file = "training.1600000.processed.noemoticon.csv"
clean_csv = 'clean_model_tweets.csv'

def main():
    cols = ['sentiment','id','date','query_string','user','text']
    df = pd.read_csv(training_file, engine='python', header=None, names=cols)
    df.drop(['id','date','query_string','user'],axis=1,inplace=True)
    print(df.sentiment.value_counts())
    df['pre_clean_len'] = [len(t) for t in df.text]
    
    data_dict = {
        'sentiment':{
            'type':df.sentiment.dtype,
            'description':'sentiment class - 0:negative, 1:positive'
        },
        'text':{
            'type':df.text.dtype,
            'description':'tweet text'
        },
        'pre_clean_len':{
            'type':df.pre_clean_len.dtype,
            'description':'Length of the tweet before cleaning'
        },
        'dataset_shape':df.shape
    }
    #pprint(data_dict)

   # distribution of length of strings in each entry.
#    fig, ax = plt.subplots(figsize=(5, 5))
#    plt.boxplot(df.pre_clean_len)
#    plt.show()

    #print(df[df.pre_clean_len > 140].head(10))
    #print(df.text[279])

    nums = [0,1600000]
    print("Cleaning and parsing the tweets...\n")
    clean_tweet_texts = []
    for i in range(nums[0],nums[1]):
        if((i+1)%100000==0): print("Tweets %d of %d have been processed" % ( i+1, nums[1] ))
        clean_tweet_texts.append(clean.clean_a_tweet(df['text'][i]))

    clean_df = pd.DataFrame(clean_tweet_texts, columns=['text'])
    clean_df['target'] = df.sentiment
    clean_df.dropna(inplace=True)
    clean_df.reset_index(drop=True,inplace=True)
    print(clean_df.info())
    clean_df.to_csv(clean_csv,encoding='utf-8')
    my_df = pd.read_csv(clean_csv,index_col=0)
    print(my_df.head())

main()
