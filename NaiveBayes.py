import numpy as np
import pandas as pd
from collections import defaultdict
import re

def clean(text):
    if pd.isnull(text):
        print("NULL VALUE: " + str(text))
    s = re.sub('[^a-z\s]+',' ', text, flags=re.IGNORECASE)
    s = re.sub('(\s+)',' ', s)
    return s

class NaiveBayes:
    def __init__(self, uniq_clases):
        self.classes = uniq_clases

    def add_to_BOW(self, example, dict_index):
        #print("example : " + example)
        if isinstance(example, np.ndarray):
            example = example[0]
        for word in example.split():
            self.bow_dict[dict_index][word] += 1

    def train(self, dataset, labels):
        self.examples = dataset
        self.labels = labels
        self.bow_dict = np.array([defaultdict(lambda:0) for i in range(self.classes.shape[0])])
        if not isinstance(self.examples, np.ndarray): self.examples = np.array(self.examples)
        if not isinstance(self.labels, np.ndarray): self.labels = np.array(self.labels)
        
        for index, category in enumerate(self.classes):
            all_category_examples = self.examples[self.labels==category]
            cleaned_examples = [clean(example) for example in all_category_examples]
            cleaned_examples = pd.DataFrame(data=all_category_examples)
            np.apply_along_axis(self.add_to_BOW, 1, cleaned_examples, index)

        # pre-compute
        prob_classes = np.empty(self.classes.shape[0])
        all_words = []
        category_word_counts = np.empty(self.classes.shape[0])
        for index, category in enumerate(self.classes):
            # prior prob p(c) for class c
            prob_classes[index] = np.sum(self.labels==category)/float(self.labels.shape[0])
            # calc total counts of all words in each class
            count = list(self.bow_dict[index].values())
            category_word_counts[index] = np.sum(np.array(list(self.bow_dict[index].values()))) + 1
            #get words of this category
            all_words += self.bow_dict[index].keys()
        #combine words of every category
        self.vocab = np.unique(np.array(all_words))
        self.vocab_len = self.vocab.shape[0]
        #denom val
        denominators = np.array([category_word_counts[index] + self.vocab_len+1 for index, cat in enumerate(self.classes)])
        # tuple
        self.categories_info = [(self.bow_dict[index], prob_classes[index], denominators[index]) for index, cat in enumerate(self.classes)]
        self.categories_info = np.array(self.categories_info)

    # estimate posterior probability of given test example
    def get_example_prob(self, test_example):
        likelihood_prob = np.zeros(self.classes.shape[0]) # store prob wrt to each class
        for index, category in enumerate(self.classes):
            for token in test_example.split():
                test_token_count = self.categories_info[index][0].get(token, 0) + 1
                test_token_prob = test_token_count/float(self.categories_info[index][2])
                likelihood_prob[index] += np.log(test_token_prob)
        post_prob = np.empty(self.classes.shape[0])
        for index, category in enumerate(self.classes):
            post_prob[index] = likelihood_prob[index] + np.log(self.categories_info[index][1])
        return post_prob
    
    def test(self, set):
        predictions = []
        for example in set:
            post_prob = self.get_example_prob(example)
            predictions.append(self.classes[np.argmax(post_prob)])
        return np.array(predictions)
        

