import numpy as np
import pandas as pd
import NaiveBayes as NB
import matplotlib.pyplot as plt

path_train_model = 'clean_model_tweets.csv'
path_clean_super_tuesday = './tweets/clean/clean_combined_super_tuesday.csv'
path_candidates = './tweets/candidates/'
path_clean = './tweets/clean/'

warren = path_clean + 'clean_Warren0.csv'
warren_after = path_clean + 'clean_Warren-after0.csv'

biden = path_clean + 'clean_Biden0.csv'
biden_after = path_clean + 'clean_Biden-after0.csv'

sanders = path_clean + 'clean_Sanders0.csv'
sanders_after = path_clean + 'clean_Sanders-after0.csv'

csv_end = '*.csv'

def train_test_split(array, split=0.1):
    indices = np.random.permutation(array.shape[0])
    split = int(split * array.shape[0])
    train_indices = indices[split:]
    test_indices = indices[:split]
    train, test = array[train_indices], array[test_indices]
    return train, test

def main():
    df = pd.read_csv(path_train_model, header=None, engine='python')
    df = df.iloc[1:] # remove first 'text' row with no data
    df = df.dropna() # drop nan rows
    data = df[[1,2]].values
    data = np.array(data)
    train, test = train_test_split(data)
    train_labels = train[:,1] # labels are the second col
    train_text = train[:,0]
    
    nb = NB.NaiveBayes(np.unique(train_labels))
    print("Starting training...")
    nb.train(train_text, train_labels)
    print("\t...training complete!")
    test_labels = test[:,1]
    test_text = test[:,0]
    p_classes = nb.test(test_text)
    accuracy = np.sum(p_classes == test_labels) / float(test_labels.shape[0])
    #print("Test set len: " + str(test_labels.shape[0]))
    print("Model accuracy: " + str(accuracy * 100.0))
    
    print("--------- Super Tuesday ---------")
    tues_df = pd.read_csv(path_clean_super_tuesday, header=None, engine='python')
    tues_df = tues_df.iloc[1:] # remove first 'text' row with no data
    tues_df = tues_df.dropna() # drop nan rows
   # print(tues_df.head())
    data = tues_df[1]
   # print(data.head())
    p_class = nb.test(data)
    #print("p_class: " + str(p_class))
    prob = np.mean(np.array(p_class).astype(np.float))
    print("Overall Twitter Super Tuesday Sentiment: " + str(prob))
    
    # --------- CANDIDATES --------- #
    print("--------- Candidates ---------")
    # WARREN
    # - before
    warren_df = pd.read_csv(warren, header=None, engine='python')
    warren_df = warren_df.iloc[1:] # remove first 'text' row with no data
    warren_df = warren_df.dropna() # drop nan rows
    data = warren_df[1]
    p_class = nb.test(data)
    w_before = p_class
    warren_before_average = np.mean(np.array(p_class).astype(np.float))
    warren_before_median = np.median(np.array(p_class).astype(np.float))
    print("- WARREN Before Sentiment:" + str(warren_before_average))
    # - after
    warren_after_df = pd.read_csv(warren_after, header=None, engine='python')
    warren_after_df = warren_after_df.iloc[1:] # remove first 'text' row with no data
    warren_after_df = warren_after_df.dropna() # drop nan rows
    data = warren_after_df[1]
    p_class = nb.test(data)
    w_after = p_class
    warren_after_average = np.mean(np.array(p_class).astype(np.float))
    warren_after_median = np.median(np.array(p_class).astype(np.float))
    print("- WARREN After Sentiment:" + str(warren_after_average))
    
    # BIDEN
    # - before
    biden_df = pd.read_csv(biden, header=None, engine='python')
    biden_df = biden_df.iloc[1:] # remove first 'text' row with no data
    biden_df = biden_df.dropna() # drop nan rows
    data = biden_df[1]
    p_class = nb.test(data)
    b_before = p_class
    biden_after_average = np.mean(np.array(p_class).astype(np.float))
    biden_before_median = np.median(np.array(p_class).astype(np.float))
    print("- BIDEN Before Sentiment:" + str(biden_after_average))
    # - after
    biden_after_df = pd.read_csv(biden_after, header=None, engine='python')
    biden_after_df = biden_after_df.iloc[1:] # remove first 'text' row with no data
    biden_after_df = biden_after_df.dropna() # drop nan rows
    data = biden_after_df[1]
    p_class = nb.test(data)
    b_after = p_class
    biden_after_average = np.mean(np.array(p_class).astype(np.float))
    biden_after_median = np.median(np.array(p_class).astype(np.float))
    print("- BIDEN After Sentiment:" + str(biden_after_average))
    
    # SANDERS
    # - before
    sanders_df = pd.read_csv(sanders, header=None, engine='python')
    sanders_df = sanders_df.iloc[1:] # remove first 'text' row with no data
    sanders_df = sanders_df.dropna() # drop nan rows
    data = sanders_df[1]
    p_class = nb.test(data)
    s_before = p_class
    sanders_before_average = np.mean(np.array(p_class).astype(np.float))
    sanders_before_median = np.median(np.array(p_class).astype(np.float))
    print("- SANDERS Before Sentiment:" + str(sanders_before_average))
    # - after
    sanders_after_df = pd.read_csv(sanders_after, header=None, engine='python')
    sanders_after_df = sanders_after_df.iloc[1:] # remove first 'text' row with no data
    sanders_after_df = sanders_after_df.dropna() # drop nan rows
    data = sanders_after_df[1]
    p_class = nb.test(data)
    s_after = p_class
    sanders_after_average = np.mean(np.array(p_class).astype(np.float))
    sanders_after_median = np.median(np.array(p_class).astype(np.float))
    print("- SANDERS After Sentiment:" + str(sanders_after_average))
    
    datas = [np.array(w_before).astype(np.float), np.array(w_after).astype(np.float)]
    box = plt.boxplot(datas, showmeans=True, showfliers=True, showcaps=True, showbox=True, whis=99)
#    plt.setp(box['boxes'][0], color='blue')
#    plt.setp(box['caps'][0], color='blue')
#    plt.setp(box['whiskers'][0], color='blue')
#    plt.setp(box['boxes'][1], color='red')
#    plt.setp(box['caps'][1], color='red')
#    plt.setp(box['whiskers'][1], color='red')
    plt.ylim([0, 4]) # y axis gets more space at the extremes
    plt.grid(True, axis='y') # let's add a grid on y-axis
    plt.title('Super Tuesday Twitter Sentiment For Warren', fontsize=18) # chart title
    plt.ylabel('Sentiment Range') # y axis title
    plt.xticks([1,2], ['Before','After']) # x axis labels
    plt.show()
    
    datas =  [np.array(b_before).astype(np.float), np.array(b_after).astype(np.float)]
    box = plt.boxplot(datas, showmeans=True, showfliers=True, showcaps=True, showbox=True, whis=99)
#    plt.setp(box['boxes'][0], color='blue')
#    plt.setp(box['caps'][0], color='blue')
#    plt.setp(box['whiskers'][0], color='blue')
#    plt.setp(box['boxes'][1], color='red')
#    plt.setp(box['caps'][1], color='red')
#    plt.setp(box['whiskers'][1], color='red')
    plt.ylim([0, 4]) # y axis gets more space at the extremes
    plt.grid(True, axis='y') # let's add a grid on y-axis
    plt.title('Super Tuesday Twitter Sentiment For Biden', fontsize=18) # chart title
    plt.ylabel('Sentiment Range') # y axis title
    plt.xticks([1,2], ['Before','After']) # x axis labels
    plt.show()
    
    datas =  [np.array(s_before).astype(np.float), np.array(s_after).astype(np.float)]
    box = plt.boxplot(datas, showmeans=True, showfliers=True, showcaps=True, showbox=True, whis=99)
#    plt.setp(box['boxes'][0], color='blue')
#    plt.setp(box['caps'][0], color='blue')
#    plt.setp(box['whiskers'][0], color='blue')
#    plt.setp(box['boxes'][1], color='red')
#    plt.setp(box['caps'][1], color='red')
#    plt.setp(box['whiskers'][1], color='red')
    plt.ylim([0, 4]) # y axis gets more space at the extremes
    plt.grid(True, axis='y') # let's add a grid on y-axis
    plt.title('Super Tuesday Twitter Sentiment For Sanders', fontsize=18) # chart title
    plt.ylabel('Sentiment Range') # y axis title
    plt.xticks([1,2], ['Before','After']) # x axis labels
    plt.show()
    
main()


#
#Model accuracy: 78.26798917493234
#--------- Super Tuesday ---------
#Overall Twitter Super Tuesday Sentiment: 2.8265147248815716
#--------- Candidates ---------
#- WARREN Before Sentiment:2.1602373887240356
#- WARREN After Sentiment:1.9725824379399777
#- BIDEN Before Sentiment:2.6969809914275067
#- BIDEN After Sentiment:2.7054023983187045
#- SANDERS Before Sentiment:1.9725621060437524
#- SANDERS After Sentiment:1.8831819024661598
#
