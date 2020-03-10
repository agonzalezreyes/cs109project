import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
# local files
import clean

path_clean_csv = 'clean_model_tweets.csv'
path_super_tuesday = './tweets/super_tuesday/combined_super_tuesday.csv'
path_candidates = './tweets/candidates/'
path_clean = './tweets/clean/clean_'
csv_end = '*.csv'

def main():
    files_candidates = glob.glob(path_candidates + csv_end)
    before_files = [file_name for file_name in files_candidates if "after" not in file_name]
    after_files = [file_name for file_name in files_candidates if "after" in file_name]
#    print(before_files)
#    print(after_files)
    all_files_candidates = before_files + after_files
    for file in all_files_candidates:
        create_clean_file(file)
    create_clean_file(path_super_tuesday)

def create_clean_file(file):
    data = pd.read_csv(file, header=None, engine='python')
    print(data.head())
    tweets = data.iloc[:,1]
    clean_tweet_texts = clean.clean_tweets(tweets)
    clean_df = pd.DataFrame(clean_tweet_texts, columns=['text'])
    clean_df.dropna(inplace=True)
    clean_df.reset_index(drop=True,inplace=True)
    print(clean_df.info())
    base_file_name = os.path.basename(file)
    file_name = path_clean + base_file_name
    clean_df.to_csv(file_name,encoding='utf-8')
    my_df = pd.read_csv(file_name,index_col=0)
    print(my_df.head())

def matrix():
    # matrix
    my_df = pd.read_csv(path_clean_csv,index_col=0)
    print(my_df.head())
    neg_doc_matrix = cvec.transform(my_df[my_df.target == 0].text)
    pos_doc_matrix = cvec.transform(my_df[my_df.target == 1].text)
    neg_tf = np.sum(neg_doc_matrix,axis=0)
    pos_tf = np.sum(pos_doc_matrix,axis=0)
    neg = np.squeeze(np.asarray(neg_tf))
    pos = np.squeeze(np.asarray(pos_tf))
    term_freq_df = pd.DataFrame([neg,pos],columns=cvec.get_feature_names()).transpose()

def word_cloud():
    neg_tweets = my_df[my_df.target == 0]
    neg_string = []
    for t in neg_tweets.text:
        neg_string.append(t)
    neg_string = pd.Series(neg_string).str.cat(sep=' ')
    from wordcloud import WordCloud

    wordcloud = WordCloud(width=1600, height=800,max_font_size=200).generate(neg_string)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

main()
