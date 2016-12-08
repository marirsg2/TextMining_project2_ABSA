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

    def extract_aspects(self, source = None):
        if source == None:
            source = self.source
        self.aspects = {}
        reviews = source['sentences']['sentence']
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
        return self.aspects
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

    def aspects_performance(self, test_source):
        aspects = self.extract_aspects()
        # print (aspects['screen'])
        # print ('screen' in aspects)
        # print (len(aspects))
        test_aspects = self.extract_aspects(test_source)
        print (len(test_aspects))

        cnt = 0
        for aspect in test_aspects:
            if aspect in aspects:
                cnt += 1
            #else:
            #    print (aspect)

        #print (len(aspects))
        print (cnt)
        print (len(test_aspects))

        return float(cnt) / float(len(test_aspects))

#Functions from here are made for task 2
#modified at Sat Dec  3 13:39:26 2016

    def __get_word_by_address(self,dep, pos):
        for word in dep:
            if word['address'] == pos:
                return word

    def get_pair_polarity(self):
        res = []
        for s in self.source['sentences']['sentence']:
            polarities = {}
            if 'aspectTerms' in s:
                aspects = s['aspectTerms']['aspectTerm']
                if type(aspects) is dict:
                    polarities[aspects['@term']] = aspects['@polarity']
                else:
                    for aspect in aspects:
                        polarities[aspect['@term']] = aspect['@polarity']

            for dep in s['DEPStagging']:
                for word in dep:
                    tmpword = word['word']
                    if 'compound' in word['deps']:
                        for pos in word['deps']['compound']:
                            tmpword = self.__get_word_by_address(dep, pos)['word'] + ' ' + tmpword
                        if len(word['deps']['compound']) > 1:
                            print (tmpword)
                    for pos in word['deps']['amod']:
                        if tmpword in polarities:
                            p = polarities[tmpword]
                            ty = 0
                            if p == 'positive':
                                ty = 1
                            elif p == 'negative':
                                ty = -1
                            else:
                                ty = 0
                            tmp = [self.__get_word_by_address(dep, pos)['word'], tmpword, ty]
                            if tmp not in res:
                                res.append(tmp)

        return res
    
    def get_adj_polarity(self):
        adjs = self.get_adj_polarity_count()
        res = {}
        for adj, v in adjs.items():
            res[adj] = (float(-v[0] + v[2])) / (float(v[0] + v[1] + v[2]))
        return res


    def get_adj_polarity_count(self):
        pair_res = self.get_pair_polarity()
        adjs = {}
        for adj in pair_res:
            if adj[0] not in adjs:
                adjs[adj[0]] = [0,0,0]
            adjs[adj[0]][adj[2] + 1] += 1

        return adjs
