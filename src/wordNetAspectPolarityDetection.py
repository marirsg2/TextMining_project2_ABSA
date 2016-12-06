'''
Created on Dec 2, 2016

@author: marir
'''

from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn
import nltk.stem
import math

import UtilityFunctions as util

# dictionary = PyDictionary()
# print(dictionary.googlemeaning("delighted"))
# print(wn.synsets("delighted")[0].definition())

'''
The choice of words for polarity were decided from the following information and logic
#https://en.wikipedia.org/wiki/Contrasting_and_categorization_of_emotions

# if any of these words are in the definition, then it affects the polarity. Keep in mind negations ("not happy")
# the keywords were also filled with common positive, negative words like good and bad (not emotions) but
# general object qualifiers (adjectives)

'''

NO_VALID_ADDRESS = -1

#also if the words are not positive or negative, then it is given neutral polarity.
#------------------------------------------------------------------------------ 
# get the polarity of adjective words from the training data
# Store the words and the counts of when it was positive, negative and neutral
# eg: "okay" : (5,1,20) 
trainingDataSeedWords = {} #
#then break the words into positive, negative and neutral words by choosing the most frequent polarity 


#===============================================================================
# 
#===============================================================================

def getDependencyTaggingWordLemmas(aspectWord,singleReview,lemmatizer):
    '''
    @summary: identifying qualifier words with dependency parsed information
    '''

    #find the DEPS address(es), the word can appear more than once
    singleAspectDepsAddresses = []
    negatedAddresses = [] #if a word has one of these addresses its meaning has been negated/changed by "No, Not" etc.
    for depsSentenceIndex in range(0,len(singleReview['DEPStagging'])):
        depsSentence = singleReview['DEPStagging'][depsSentenceIndex ]
        for depsNode in depsSentence[1:] : #we skip the first one which is the root node
            if depsNode['rel'] == 'neg': #then this negates another word (either an adjective or verb)
                negatedAddresses.append(depsNode['head'])                    
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
                    qualifyingWordTuples.append( (sentenceIndex, singleNode['word'],singleNode['tag'],singleNode['address']) )
            #end if the address was the adj modifier address
            elif singleNode['head'] == aspectAddress:
                if singleNode['tag'] in ["JJ", "JJR", "JJS" ]:
                    qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag'],singleNode['address']))                            
            #if it is an adjective , check if it was within 3 distance away and NOT pointing to another nsubj
            elif singleNode['tag'] in ["JJ", "JJR", "JJS"]:                        
                #check if it does not modify another noun
                try:
                    nounSubjects = singleNode['deps']['nsubj']                             
                    if  aspectAddress in nounSubjects:  #check if it is the subject before checking for noun modifier                                          
                        qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag'], singleNode['address']))
                        continue
                    else:
                        continue #the nsubj is another, skip this word, back to for loop
                except:
                    pass
                try:
                    nounModifiers = singleNode['deps']['nmod']       
                    if aspectAddress in nounModifiers:                                            
                        qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag'],
                                                     singleNode['address']))
                        continue
                    else:
                        continue #the nsubj is another, skip this word, back to for loop
                except:
                    pass
                #if we made it here for this case, then the adjective is close to the aspect , and does not qualify
                # any other noun, then take it as valid
                if  abs(singleNode['address'] -  aspectAddress) <= 3:
                    qualifyingWordTuples.append((sentenceIndex, singleNode['word'],singleNode['tag'], 
                                                 singleNode['address']))                        
            #END elif singleNode['tag'] in ["JJ", "JJR", "JJS"]:
        #END FOR loop through the DEPS node
    #END FOR loop through the singleAspectDepsAddresses
    #------------------------------------------------------------------------------ 
    #At this point we have all the qualifying words for the aspect
    lemmaWordsList = []
    for singleQualifierTuple in qualifyingWordTuples:
        lemmaWord = lemmatizer.lemmatize(singleQualifierTuple[1])
        if singleQualifierTuple[3] in negatedAddresses:
            lemmaWord = "-" + lemmaWord 
        #singleQualifierTuple.append(lemmaWord)
        #lemmaWordsList.append(singleQualifierTuple)
        lemmaWordsList.append(lemmaWord)
    
    return lemmaWordsList

#===============================================================================
# 
#===============================================================================

def getPosTaggingWordLemmas(aspectWord,singleReview,lemmatizer):
    '''
    @summary: identifying qualifier words with dependency parsed information
    '''

    #find the DEPS address(es), the word can appear more than once
    lemmaWordsList = []    
    aspectIndexList = []
    for posSentenceIndex in range(0,len(singleReview['POStaggedText'])):
        posSentence = singleReview['POStaggedText'][posSentenceIndex ]        
        for posNodeIndex in range(0,len(posSentence)): 
            posNode = posSentence[posNodeIndex]
            if posNode[0] == aspectWord:
                aspectIndexList.append(posNodeIndex)
        #END for loop through the pos nodes
        #find the preceeding adjective or an adjective within 4 words after
        for aspectIndex in aspectIndexList:
            leftLimit = aspectIndex-4
            rightLimit = aspectIndex + 4            
            for sentenceIndex in range(leftLimit,rightLimit+1):
                if sentenceIndex >=0 and sentenceIndex < len(posSentence):               
                    #if it is an adjective it maybe a qualifier word
                    if posSentence[sentenceIndex][1] in  ["JJ", "JJR", "JJS" ]:
                        nextWordIndex = sentenceIndex +1 
                        if nextWordIndex < len(posSentence) and nextWordIndex != aspectIndex:
                            #if the next word is a noun that is not the aspect, then the adjective qualifies the next word
                            if not posSentence[sentenceIndex][1] in  ["NN", "NNS"]:
                                lemmaWord = lemmatizer.lemmatize(posSentence[sentenceIndex][0])                                
                                if sentenceIndex >= 1 and posSentence[sentenceIndex][0].lower() in  ["not", ",not" , "no", ",no" ,"never", ",never" ]:
                                    lemmaWord = "-" + lemmaWord                             
                                lemmaWordsList.append(lemmaWord)                                                          
                        else: #the next word is not an noun, and the adjective is within 4 words of the aspect noun. 
                            lemmaWord = lemmatizer.lemmatize(posSentence[sentenceIndex][0])
                            if sentenceIndex >= 1 and posSentence[sentenceIndex][0].lower() in  ["not", ",not" , "no", ",no" ,"never", ",never" ]:
                                lemmaWord = "-" + lemmaWord                                                        
                            lemmaWordsList.append(lemmaWord)
                    elif posSentence[sentenceIndex][0].startswith(","):
                        break; #new sentence clause, less confidence that adjective was connected. 

    if len(lemmaWordsList) > 1:
        print("found multiple adjectives for the aspect in the sentence")
        print(singleReview['text'])
        print(aspectWord,lemmaWordsList)
    
    return lemmaWordsList

#===============================================================================
# 
#===============================================================================

def getDefiningWords(lemmaSet,lemmatizer,depth=1, englishDictionary = None):
    '''
    @summary: gets the words related to the definition of the lemma, and then see the definitions
    for each of the words in the original definition. Repeat for the specified depth.
    removes trivial words like a,the,of, it, etc.
    '''
    trivialLowerCaseWords = ['a','of','the', 'it', 'of', 'which', 'who', 'what', 'when', 'i', 'you', 'he', 'she', 'then', 'before',
                             'after','or','and', 'to']
    
    definitionWordTokens = set()
    for singleLemma in lemmaSet:
        try:
            wordNetDefinition = wn.synsets(singleLemma)[0].definition()
            definitionWordTokens =  definitionWordTokens.union(set(util.getNormalized_text(wordNetDefinition)))
        except:
            pass #no wordnet definitions                 
        try:
            dictionaryDefinition = englishDictionary.googlemeaning(singleLemma)            
            dictionaryDefinition = dictionaryDefinition.split("\n")[1]
            definitionWordTokens= definitionWordTokens.union(set(util.getNormalized_text(dictionaryDefinition)))
        except:
            pass # if no english dictionary, just use wordnet
        #END IF
        definitionWordTokens= set(definitionWordTokens)
        definitionWordTokens = set([lemmatizer.lemmatize(x) for x in definitionWordTokens])
    if depth > 0:
        definitionWordTokens = definitionWordTokens.union(
            getDefiningWords(definitionWordTokens, lemmatizer,depth-1, englishDictionary))
    
    return definitionWordTokens
    
    

#===============================================================================
# 
#===============================================================================

def getDictionaryPolarity(lemmaSet, lemmatizer, singleReview, positiveAssociationWords,
                          negativeAssociationWords,neutralWords,englishDictionary):
    '''
    @summary: 
        1) For each qualifier word determine the polarity by looking at it's definition. If the definition does not exist, ignore
        2) if it exists, get all the words and lemmatize them. Score the number of pos, neg, and neutral words
            if preceeded by not, no, never, then score oppposite. Polarity is +/-, neutral score is seperate.
            If there is a "but", "however", then the word is conflicted, simply set neutral to a negative (-1)        
    '''
    totalPolarityScore = 0
    conflicted = False
    for singleLemma  in lemmaSet:
        #get the score
        polarityScore = 0        
        polarityMultiplier = 1 #is -1 if the word was negated in the sentence
        if singleLemma.startswith("-"):
            polarityMultiplier = -1
            singleLemma[1:] #ignore the "-" 
        
        definitionLemmatizedWordTokenSet = getDefiningWords(set([singleLemma]),lemmatizer, 1,englishDictionary)

        #now count the scores
        for singleWord in definitionLemmatizedWordTokenSet:            
            scorePositiveCountMultiplier = 0
            scoreNegativeCountMultiplier = 0 # if the word was inverted with ["No", Not, "Never"] or other such words
            #check if there is polarity Change Word before the                                      
            if singleWord in positiveAssociationWords:
                polarityScore+= 1*polarityMultiplier
            elif singleWord in negativeAssociationWords:
                polarityScore -=1*polarityMultiplier            
            #if the polarity score is -ve for this lemma , but the total score so far is +ve, then the review is conflicted
            if (polarityScore >0 and totalPolarityScore <0) or (polarityScore <0 and totalPolarityScore >0):
                conflicted = True            
            polarityScore = polarityScore/polarityScore # so it will be +/- 1 
            totalPolarityScore += polarityScore
                
                
        ret_polarity = "neutral"
        if totalPolarityScore > 0:
            ret_polarity = "positive"
        elif totalPolarityScore < 0:
            ret_polarity = "negative"
        
        return (ret_polarity,conflicted, polarityScore) 
                
                

        
        
        
    

#===============================================================================
# 
#===============================================================================
def unsupervisedWordNetPolarity_updateDictWithAspectPolarityPairs(allRestaurantData, hasEnglishDict  = False):
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
            d) If we could not find adjectives for the aspect, then it is neutral
            e) Anecdotes are really hard with this method, need a lot of semantic understanding and context knowledge
        ? how to handle "I got no satisfaction from the food".
                what tag is satisfaction. Find a similar case from the review data.
                
        "I had the salmon dish and while it was fine, for the price paid, I expected it to have some type of flavor"
        "Decor is nice and minimalist, food simple yet very well presented and cooked, and the wine list matches the food very well"
                
    @todo: aspect terms can be compound words. check ifa compound word, in that case combine the qualifiers
    POS can be 4 words before but drop if NN or comma
    '''
    
    positiveAssociationWords = ["delight","elation","excitement","happiness","joy","pleasure","love","affection",
                                                "satisfaction","contentment","relaxation","relief","calmness","politeness",
                                                "happy",
                                                "good", "great", "fine", "acceptable"]
    negativeAssociationWords = ["sadness", "disappointment", "anger", "annoyance", "contempt", "irritation",
                            "anxiety", "embarrassment", "fear" , "helplessness", "powerlessness", "worry",
                            "frustration", "shame" ,"boredom", "despair", "hurt", "stress", "shock", "tension"]
    neutralWords = [ "normal", "neutral", "ok", "o.k.", "okay", ]
    polarityChangeWords = ['not', 'never', 'over', 'excess']
    
    lemmatizer = nltk.stem.WordNetLemmatizer()
    englishDictionary  = None
    if hasEnglishDict == True:
        englishDictionary = PyDictionary() #optional can be turned off    
        
    positiveAssociationWords = [lemmatizer.lemmatize(x) for x in positiveAssociationWords]
    negativeAssociationWords = [lemmatizer.lemmatize(x) for x in negativeAssociationWords]
    neutralWords = [lemmatizer.lemmatize(x) for x in neutralWords]  
    
# REMOVE ME    
#     print (positiveAssociationWords)
#     print (negativeAssociationWords)
#     print (neutralWords)
#     return
    
    #each review is a dict that contains the raw data, POS tags, DEPS (dependency parser) tags, and the 
    # actual aspects, polarity, and category for each review
    for singleReview in allRestaurantData['sentences']['sentence']:
        #first get the aspects in the sentence        
        try:
            aspectTerms = singleReview['aspectTerms']['aspectTerm']
        except:
            continue #no aspect terms
        if type(aspectTerms) == dict:
            # if there were more than one aspect term, it would be in a list
            #this just makes the single term case (which would be a dict ) into a list of one
            # so the code is common
            aspectTerms = [aspectTerms]            
        for singleAspectTermDict in aspectTerms:
            aspectWord = singleAspectTermDict['@term']  
            truePolarity = singleAspectTermDict['@polarity']            
            depsLemmaList = getDependencyTaggingWordLemmas(aspectWord,singleReview,lemmatizer)
            posLemmaList = getPosTaggingWordLemmas(aspectWord,singleReview,lemmatizer) 
            print("============================================================")  
            print("SENTENCE =", singleReview['text'], "\nAspect Word =", aspectWord, " Aspect Polarity =", truePolarity)
            print("DEPS lemmas =", depsLemmaList )
            print("POS lemmas =", posLemmaList )
       
            # WHY does this test case fail for "atmosphere" The design and atmosphere is just as good.  Atmosphere failed ??
    
       
            lemmaSet = set(depsLemmaList + posLemmaList)            
            (aspectPolarity ,isConflicted, polarityScore)= getDictionaryPolarity(lemmaSet,lemmatizer,
                                                   singleReview,positiveAssociationWords,negativeAssociationWords,neutralWords,
                                                   englishDictionary)
            print (aspectPolarity ,isConflicted, polarityScore)
             
             

                
                            
                            
                                
                                     
                        

  
                             
             
        
        

