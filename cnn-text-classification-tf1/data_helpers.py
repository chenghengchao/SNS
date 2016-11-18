import numpy as np
import re
import itertools
from collections import Counter
import os

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(open(positive_data_file, "r").readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "r").readlines())
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]


def load_data():
    """
    load file
    """
    #print data_class + " data is loaded ..." 
    pos_path = r'/mydata/pos'
    neg_path = r'/mydata/neg'
    pos_file_path = os.getcwd() + pos_path 
    neg_file_path = os.getcwd() + neg_path 
    #print file_path + " is the dir..." 
    for filename in os.listdir(pos_file_path):
    #    print "extract data from " + filename
        data = list(open(pos_file_path + '/' + filename, "r").readlines())
    data = [s.strip() for s in data]
    pos_x_text = [clean_str(sent) for sent in data] 
    pos_cls = [[0, 1] for _ in data]
    data = []
    for filename in os.listdir(neg_file_path):
    #    print "extract data from " + filename
        data = list(open(neg_file_path + '/' + filename, "r").readlines())
    data = [s.strip() for s in data]
    neg_x_text = [clean_str(sent) for sent in data] 
    neg_cls = [[0, 1] for _ in data]
    x_text = pos_x_text +  neg_x_text
    y = np.concatenate([pos_cls, neg_cls], 0)
    print len(x_text)
    print len(y)
    return [x_text, y]



def load_data2():
    """
    load file
    """
    #print data_class + " data is loaded ..." 
    pos_path = r'/mydata/pos'
    neg_path = r'/mydata/neg'
    pos_file_path = os.getcwd() + pos_path 
    neg_file_path = os.getcwd() + neg_path 
    #print file_path + " is the dir..." 
    fpos = open("posfile.txt", "a")
    for filename in os.listdir(pos_file_path):
    #    print "extract data from " + filename
        for data in open(pos_file_path + '/' + filename, "r"):
            fpos.write(data)
            fpos.write("\n")
    fpos.close()
    #data = list(open())
    data = []
    fneg = open("negfile.txt", "a")
    for filename in os.listdir(neg_file_path):
    #    print "extract data from " + filename
        for data in open(neg_file_path + '/' + filename, "r"):
            fneg.write(data)
            fneg.write("\n")
    fneg.close()



if __name__ == '__main__':
    x, y = load_data2()
    #print x
    #print y
