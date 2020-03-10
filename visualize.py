import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from wordcloud import WordCloud
from pylab import *
import seaborn as sns

# local files
import clean
import bagofwords

path_clean_csv = 'clean_model_tweets.csv'
path_clean_super_tuesday = './tweets/clean/clean_combined_super_tuesday.csv'
path_candidates = './tweets/candidates/'
path_clean = './tweets/clean/'
warren = path_clean + 'clean_Warren0.csv'
csv_end = '*.csv'
stop_words = ["super tuesday", "super", "tuesday", "supertuesday"] + clean.stop_words
num_top = 500

def main():
    supertuesday_df = super_tues()
    warren_df = df_for_file(warren, name="Warren (before results)")
    #top_words_for_df(warren_df, title=": Warren (before results)")
    supertuesday_df = supertuesday_df[2:] # remove super tuesday words rows
    #top_words_for_df(supertuesday_df, title="Super Tuesday (before results)")
    #correlation_visualize(supertuesday_df, warren_df, first="Warren (before)", second="Super Tuesday (before)")

def correlation_visualize(df1, df2, first="", second=""):
#    plt.figure(figsize=(8,6))
#    ax = sns.regplot(x=df1['freq'], y=df2['freq'],fit_reg=False, scatter_kws={'alpha':0.5})
#    plt.ylabel(first + ' Frequency')
#    plt.xlabel(second + ' Frequency')
#    plt.title( first + ' Frequency vs ' + second + ' Frequency')
#    plt.show()
    pass 

def top_words_for_df(df, title=""):
    df = df.iloc[1:]
    y_pos = np.arange(50)
    plt.figure(figsize=(12,12))
    plt.bar(y_pos, df.sort_values(by='freq', ascending=False)['freq'][:50], align='center', alpha=0.5)
    plt.xticks(y_pos, df.sort_values(by='freq', ascending=False)[:50].word, rotation='vertical')
    plt.ylabel('Frequency')
    plt.xlabel('Top 50 tokens')
    plt.title('Top 50 tokens in tweets ' + title)
    plt.gcf().subplots_adjust(bottom=0.35)
    plt.show()

def df_for_file(file_name, name):
    df = pd.read_csv(file_name, header=None, engine='python')
    df = df.iloc[1:] # remove first 'text' row with no data
   # print(df.head())
    tweets = df[1]
    strings = []
    for t in tweets: strings.append(t)
    strings = pd.Series(strings).str.cat(sep=' ')
    #word_cloud(strings, category=name)
    top_df = bagofwords.freq_df(tweets, num=num_top)
    #print(top_df)
    #zipf_bar(top_df, num=50, category=name)
    #zipf_log(top_df, num=num_top, category=name)
    return top_df

def super_tues():
    df = pd.read_csv(path_clean_super_tuesday, header=None, engine='python')
    df = df.iloc[1:] # remove first 'text' row with no data
   # print(df.head())
    tweets = df[1]
    strings = []
    for t in tweets: strings.append(t)
    strings = pd.Series(strings).str.cat(sep=' ')
    #word_cloud(strings, category="Super Tuesday")
    top_df = bagofwords.freq_df(tweets, num=num_top)
   # print(top_df)
    #zipf_bar(top_df, num=num_top, category="(Super Tuesday)")
    #zipf_log(top_df, num=num_top, category="(Super Tuesday)")
    return top_df

def zipf_bar(data, num=20, category=""):
    y_pos = np.arange(num)
    plt.figure(figsize=(10,8))
    s = 1
    expected_zipf = [data.sort_values(by='freq', ascending=False)['freq'][0]/(i+1)**s for i in y_pos]
    plt.bar(y_pos, data.sort_values(by='freq', ascending=False)['freq'][:num], align='center', alpha=0.5)
    plt.plot(y_pos, expected_zipf, color='r', linestyle='--',linewidth=2,alpha=0.5)
    plt.ylabel('Frequency')
    plt.title('Top ' + str(num) + ' tokens in tweets ' + category)
    plt.show()

def zipf_log(term_freq_df, num=20, category=""):
    counts = term_freq_df.freq
    tokens = term_freq_df.word
    ranks = arange(1, len(counts)+1)
    indices = argsort(-counts)
    frequencies = counts[indices]
    plt.figure(figsize=(6,6))
    plt.ylim(1,10**5)
    plt.xlim(1,10**5)
    loglog(ranks, frequencies, marker=".")
    plt.plot([1,frequencies[0]],[frequencies[0],1],color='r')
    title("Zipf plot for " + str(num) + " tweets tokens " + category)
    xlabel("Frequency rank of token")
    ylabel("Absolute frequency of token")
    grid(True)
    for n in list(logspace(-0.5, log10(len(counts)-2), 25).astype(int)):
        dummy = text(ranks[n], frequencies[n], "",
                     verticalalignment="bottom",
                     horizontalalignment="left") #" " + tokens[indices[n]],
    plt.show()

def word_cloud(strings, category=""):
    wordcloud = WordCloud(stopwords=stop_words, width=1600, height=800,max_font_size=200).generate(strings)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Top words ' + category)
    plt.show()

main()
