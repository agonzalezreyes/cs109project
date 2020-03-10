import csv
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import glob
import os
import clean
import collections
import itertools

path_candidates = "./tweets/candidates/"
path_tues = "./tweets/super_tuesday/"
csv_path = "*.csv"
output_path = "./output/"
combined_path = path_tues + "combined_super_tuesday.csv"

def main():
    files_candidates = glob.glob(path_candidates + csv_path)
    #base_files = [os.path.basename(file) for file in files]
    print(files_candidates)
    before_files = [file_name for file_name in files_candidates if "after" not in file_name]
    after_files = [file_name for file_name in files_candidates if "after" in file_name]
    print(before_files)
    print(after_files)
    all_files_candidates = before_files + after_files
    #process_files(all_files)

    files_tuesday = glob.glob(path_tues + csv_path)
    print(files_tuesday)
    # merge all super tuesday files
    with open(combined_path, 'a') as singleFile:
        for file in files_tuesday:
            for line in open(file, 'r'):
                singleFile.write(line)

def process_files(files):
    for file in before_files:
        data = pd.read_csv(file, delimiter=',', header=None)
        tweets = data.iloc[:,1]
        cleaned_tweets = clean.clean_tweets(tweets)
        bigrams_from_tweets = clean.create_bigrams(cleaned_tweets)
        bigrams = list(itertools.chain(bigrams_from_tweets))
        bigram_counts = collections.Counter(bigrams)# Create counter of words in clean bigrams
        top_bigrams = bigram_counts.most_common(15)
        save_output(file, top_bigrams)
        create_graph(file, top_bigrams)

def save_output(file_name, text):
    base_file = os.path.basename(file_name)
    with open(output_path + base_file[:-4] + "-output.txt", "w") as text_file:
        text_file.write(str(text))

def create_graph(file_name, bigrams):
    bigram_df = pd.DataFrame(bigrams, columns=['bigram', 'count'])
    print(bigram_df)
    d = bigram_df.set_index('bigram').T.to_dict('records')
    G = nx.Graph()
    for k, v in d[0].items():
        G.add_edge(k[0], k[1], weight=(v * 10.0))
    print("G num nodes: " + str(len(G)))
    fig, ax = plt.subplots(figsize=(8,8))
    pos = nx.spring_layout(G, k=2.5)
    nx.draw_networkx(G, pos, node_size= 90.0, font_size=8, width=3, edge_color='grey', node_color='blue', with_labels=False, ax=ax)
    for key, value in pos.items():
        x,y = value[0] , value[1]
        ax.text(x, y, s=key, bbox=dict(alpha=0.25), horizontalalignment='center', fontsize=10)
   # plt.show()
    base_file = os.path.basename(file_name)
    fig.savefig(output_path + base_file[:-4] + ".png")

if __name__ == '__main__':
    main()
