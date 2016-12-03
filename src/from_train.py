'''
#modified at Mon Nov 28 02:52:50 2016
This class is used for all of the information extracted from the training data
The possibility of an aspect is an aspect is useless I think
'''
import operator

class FromTrain:

    def __init__(self, source):
        self.source = source

    def __plus_one(self, term):
        if term in self.aspects:
            self.aspects[term] += 1
        else:
            self.aspects[term] = 1

    def extract_aspects(self):
        self.aspects = {}
        reviews = self.source['sentences']['sentence']
        cnt = 0
        for review in reviews:
            cnt += 1
            if 'aspectTerms' in review:
                aspects = review['aspectTerms']['aspectTerm']
                if type(aspects) is dict:
                    self.__plus_one(aspects['@term'])
                else:
                    for aspect in aspects:
                        self.__plus_one(aspect['@term'])

        print ('%d' % cnt + ' reviews counted')
        return sorted(self.aspects.items(), key=operator.itemgetter(1), reverse = True)


    def aspects_possibility(self):
        aspects = {}
        reviews = self.source['sentences']['sentence']
        for review in reviews:
            for aspect in self.aspects:
                if aspect in review['text']:
                    #using two spaces before and after a word to make sure
                    #this is a word
                    if ' ' + aspect + ' ' in aspects:
                        aspects[aspect] += 1
                    else:
                        aspects[aspect] = 1

        for aspect in self.aspects:
            aspects[aspect] = float(aspects[aspect]) / float(self.aspects[aspect])
            if aspects[aspect] > 1.0:
                print(aspect, self.aspects[aspect], aspects[aspect])

        return aspects

#Functions from here are made for task 2
#modified at Sat Dec  3 13:39:26 2016
    def get_adj_plority(self):
        for s in self.source['sentences']['sentence']:
            print (s)

