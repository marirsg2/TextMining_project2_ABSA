'''
Created on Dec 2, 2016

@author: marir
'''

from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn

# dictionary = PyDictionary()
# print(dictionary.googlemeaning("delighted"))
# print(wn.synsets("delighted")[0].definition())

#https://en.wikipedia.org/wiki/Contrasting_and_categorization_of_emotions
# if any of these words are in the definition, then it affects the polarity. Keep in mind negations ("not happy")
# the keywords were also filled with common positive, negative words like good and bad (not emotions) but
# general object qualifiers (adjectives)
positiveAssociationWords = ["delight","elation","excitement","happiness","joy","pleasure","love","affection",
                                                "satisfaction","contentment","relaxation","relief","calmness","politeness",
                                                "happy",
                                                "good", "great", "fine", "acceptable"]
negativeAssociationWords = ["sadness", "disappointment", "anger", "annoyance", "contempt", "irritation",
                            "anxiety", "embarrassment", "fear" , "helplessness", "powerlessness", "worry",
                            "frustration", "shame" ,"boredom", "despair", "hurt", "stress", "shock", "tension"]
neutralWords = [ "normal", "neutral", "ok", "o.k.", "okay", ]

adjectivePolaritySwitchers = ['not', 'never', 'over', 'excess']

#also if the words are not positive or negative, then it is given neutral polarity.
#------------------------------------------------------------------------------ 
# get the polarity of adjective words from the training data
# Store the words and the counts of when it was positive, negative and neutral
# eg: "okay" : (5,1,20) 
trainingDataSeedWords = {} #
#then break the words into positive, negative and neutral words by choosing the most frequent polarity 


'''

'''
#===============================================================================
# 
#===============================================================================
def unsupervisedWordNetPolarity_updateDictWithAspectPolarityPairs(allRestaurantData):
    '''
    @summary: Now load the reviews with deps parsing, and ASSUME the aspect is known. Find the adjective
qualifying the aspect. Then apply the dictionary search. Can also be an adverb , if the aspect is the noun subject eg: food is great.
NOTE: if no amod or nsubj connection, find the nearest JJ that has the "head" as the aspect and not connected to anything else
NOTE: if the aspect is not literally there in the sentence, then this approach cannot work
IMPORTANT: Can be "little perks were great" little is amod, so is great. Read through and id all JJ with nsubj as aspect.
NOTE: if the adj is not linked in DEPS tags, then look for the adjectives around the aspect word,
IMPORTANT: look for negation words with 2 words before it ? Or can you use the tree?
dictionary search: Get the definition, do dependency parsing.
        Then for each adjective, 
            a) see if it is negated. 
            b) get the lemma form and see if it is in the assoc list
            c) if the words in the association list appear directly in the definition.
                    also be careful of negations "without pleasure" , "no satisfaction" ,"not good"
                    I think those are all the words

        ? how to handle "I got no satisfaction from the food".
                what tag is satisfaction. Find a similar case from the review data.
                
        "I had the salmon dish and while it was fine, for the price paid, I expected it to have some type of flavor"
        "Decor is nice and minimalist, food simple yet very well presented and cooked, and the wine list matches the food very well"
                
    '''
    #each review is a dict that contains the raw data, POS tags, DEPS (dependency parser) tags, and the 
    # actual aspects, polarity, and category for each review
    for singleReview in allRestaurantData['sentences']['sentence']:
        #first get the aspects in the sentence
        aspectList = []
        print("a")
        
        

