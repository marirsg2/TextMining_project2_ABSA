'''
#modified at Mon Nov 28 01:03:16 2016
This class is used for all of the information extracted from the training data

'''
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

        return self.aspects
