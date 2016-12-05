'''
Created on Dec 2, 2016

@author: marir
'''

from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn
import nltk.stem
import math

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

NO_VALID_ADDRESS = -1

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
    @summary: Now load the reviews with deps parsing, and ASSUME the aspect is known. 

Find the adjective
qualifying the aspect. Then apply the dictionary search. Can also be an adverb , if the aspect is the noun subject eg: food is great.

NOTE: if no amod or nsubj connection, find the nearest JJ that has the "head" as the aspect and not connected to anything else
IMPORTANT: Can be "little perks were great" little is amod, so is great. Read through and id all JJ with nsubj as aspect.

NOTE: if the aspect is not literally there in the sentence, then this approach cannot work

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
    lemmatizer = nltk.stem.WordNetLemmatizer()
    
    #each review is a dict that contains the raw data, POS tags, DEPS (dependency parser) tags, and the 
    # actual aspects, polarity, and category for each review
    for singleReview in allRestaurantData['sentences']['sentence']:
        #first get the aspects in the sentence
        aspectTerms = singleReview['aspectTerms']['aspectTerm']
        if type(aspectTerms) == dict:
            # if there were more than one aspect term, it would be in a list
            #this just makes the single term case (which would be a dict ) into a list of one
            # so the code is common
            aspectTerms = [aspectTerms]            
        for singleAspectTermDict in aspectTerms:
            aspectWord = singleAspectTermDict['@term']
            truePolarity = singleAspectTermDict['@polarity']
            #find the DEPS address(es), the word can appear more than once
            singleAspectDepsAddresses = []
            for depsSentenceIndex in range(0,len(singleReview['DEPStagging'])):
                depsSentence = singleReview['DEPStagging'][depsSentenceIndex ]
                for depsNode in depsSentence[1:] : #we skip the first one which is the root node
                    if depsNode['word'] == aspectWord:
                        amodAddress =  [] # -1 means no address
                        try:
                            amodAddress = depsNode['deps']['amod']
                        except:
                            amodAddress =  []  
                            
                        #append the tuple of the aspect word and the adj modifier
                        singleAspectDepsAddresses.append((depsSentenceIndex,depsNode['address'],amodAddress))                                             
                #END FOR loop through the deps nodes
            #END FOR loop through the deps sentences
            #------------------------------------------------------------------------------ 
            #NOW determine the polarity of the aspect word
            qualifyingWordTuples = [] # each entry is (sentenceIndex, wordAddress, word)
            for (sentenceIndex, aspectAddress,amodAddresses) in singleAspectDepsAddresses:                                
                #note the deps parser address does not always match the list index. so iterate through nodes 
                for singleNode in singleReview['DEPStagging'][sentenceIndex]:
                    #CHECK if the node matches our adjective mod address
                    if singleNode['address'] in amodAddresses: #If amod was -1, then we wont find one
                        if singleNode['tag'] not in ["JJ", "JJR", "JJS"]:
                            print("Error , incorrect DEPS tree connection with amod")
                        else:
                            qualifyingWordTuples.append( (sentenceIndex, singleNode['word'],singleNode['tag']) )
                    #end if the address was the adj modifier address
                    elif singleNode['head'] == aspectAddress:
                        if singleNode['tag'] in ["JJ", "JJR", "JJS" ]:
                            qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag']))                            
                    #if it is an adjective , check if it was within 3 distance away and NOT pointing to another nsubj
                    elif singleNode['tag'] in ["JJ", "JJR", "JJS"]:                        
                        #check if it does not modify another noun
                        try:
                            nounSubjects = singleNode['deps']['nsubj']                             
                            if  aspectAddress in nounSubjects:  #check if it is the subject before checking for noun modifier                                          
                                qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag']))
                                continue
                            else:
                                continue #the nsubj is another, skip this word, back to for loop
                        except:
                            pass
                        try:
                            nounModifiers = singleNode['deps']['nmod']       
                            if aspectAddress in nounModifiers:                                            
                                qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag']))
                                continue
                            else:
                                continue #the nsubj is another, skip this word, back to for loop
                        except:
                            pass
                        #if we made it here for this case, then the adjective is close to the aspect , and does not qualify
                        # any other noun, then take it as valid
                        if  abs(singleNode['address'] -  aspectAddress) <= 3:
                            qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag']))                        
                    #END elif singleNode['tag'] in ["JJ", "JJR", "JJS"]:
                #END FOR loop through the DEPS node
            #END FOR loop through the singleAspectDepsAddresses
            #------------------------------------------------------------------------------ 
            #At this point we have all the qualifying words for the aspect
            for singleQualifierTuple in qualifyingWordTuples:
                lemmaWord = lemmatizer.lemmatize(singleQualifierTuple[1])
                
                            
                            
                                
                                     
                        

  
                             
             
        
        

