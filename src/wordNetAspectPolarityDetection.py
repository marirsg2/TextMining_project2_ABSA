'''
Created on Dec 2, 2016

@author: marir
'''

from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn

dictionary = PyDictionary()

print(dictionary.googlemeaning("delighted"))
print(wn.synsets("delighted")[0].definition())

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
#also if the words are not positive or negative, then it is given neutral polarity.
#------------------------------------------------------------------------------ 
# get the polarity of adjective words from the training data
# Store the words and the counts of when it was positive, negative and neutral
# eg: "okay" : (5,1,20) 
trainingDataSeedWords = {} #
#then break the words into positive, negative and neutral words by choosing the most frequent polarity 


#need to use dependency parsing to negate the adjectives (not, free of)
# need to get the lemma (root word)
