import json
import re
import xml.etree.ElementTree

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import RegexpTokenizer
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors.nearest_centroid import NearestCentroid

import numpy as np
import xmldict


class FileOperations:
    def __init__(self, file_name):
        self.file_name = file_name
        f = open(file_name, 'r')
        self.text = f.read()
        f.close()

    #read the json file
    def get_json(self):
        print ("Loading json...")
        self.jsons = []
        lines = self.text.split('\n');
        for line in lines:
            try:
                curr = json.loads(line)
                for i in range(len(curr)):
                    curr[i][0] = re.sub('[^a-zA-Z]+', '', curr[i][0])
                self.jsons.append(curr)
            except:
                pass

        self.num_lines = len(self.jsons)
        return self.jsons

    def get_xml(self):
        self.xml_root = xml.etree.ElementTree.parse(self.file_name).getroot()
        return self.xml_root

    
    '''
        Edit this function to extract the aspects and polarity, and all the information
    '''
    def get_sentences(self):
        sentences = []
        for sentence in self.xml_root:
            for text in sentence.findall('text'):
                sentences.append(text.text)
        return sentences
#------------------------------------------------------------------------------ 
    def convertXmlToDict(self):
        '''
        '''
        ret_xmlDict = {}
        with open(self.file_name, 'r') as content_file:
            content = content_file.read()
            ret_xmlDict = xmldict.xml_to_dict(content)
        return ret_xmlDict
            
#------------------------------------------------------------------------------ 
    def write_to_file(self, vec, file_name):
        cur = 0
        pre = 0
        f = open(file_name, 'a')
        for line in vec:
            cur += 1
            if(cur != pre):
                print (cur * 100 / len(vec), '%')
                pre = cur
            res = json.dumps(line);
            f.write(res)
            f.write('\n')
        f.close


    def get_taged_data(self):
        self.tags = []
        lines = self.text.split('\n')
        for line in lines: 
            if len(line) == 0:
                continue
            self.tags.append(json.loads(line) )
        return self.tags

    def normalize(self):
        print ("Normalizing...")
        self.text = self.text.lower()

    def remove_chars(self):
        print ('Removing...')
        

    def tokenize(self, raw):
        stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'\w+') #only alpha letters accepted
        tokens = tokenizer.tokenize(raw)
        stems = [stemmer.stem(word) for word in tokens]
        return stems

    def get_tfidf(self):
        print ("Getting TF-IDF...")
        tfidf = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
        tfs = tfidf.fit_transform(self.reviews)
        print (tfs.shape)
        return tfs

    def get_value(self):
        y = []
        for line in self.jsons:
            if int(line['overall']) > 3:
                y.append(1)
            else:
                y.append(0)
        return y

    def train_bayes_model(self, X, y):
        print ("Training Bayes model...")
        clf = MultinomialNB()
        clf.fit(X,y)
        return clf

    def score(self, clf, X, y):
        print ("Predicting...")
        res = clf.predict(X)
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        for i in range(len(res)):
            if 1 == y[i] and res[i] == 1:
                TP += 1;
            elif res[i] == 1 and y[i] == 0:
                FP += 1;
            elif res[i] == 0 and y[i] == 1:
                FN += 1;
            elif res[i] == 0 and y[i] == 0:
                TN += 1;
        return TP, FP, FN, TN

    def train_rocchio_model(self, X, y):
        print ("Training Rocchio model...")
        clf = NearestCentroid()
        clf.fit(X,y)
        return clf

