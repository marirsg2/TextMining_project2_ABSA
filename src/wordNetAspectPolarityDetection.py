'''
Created on Dec 2, 2016

@author: marir
'''

from nltk.corpus import wordnet as wn
import nltk.stem

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
    #TODO  parse the sentence definitions and only store adjectives for delving deeper. Maybe the nouns
    #     as well. As of now, we just filter from a list 
    
    trivialLowerCaseWords = set( ['a','of','the', 'it', 'of', 'which', 'who', 'what', 'when', 'i', 'you', 'he', 'she', 'then', 'before',
                             'after','or','and', 'to','with', 'an', 'not', 'cannot' , 'in' , 'can' , 'make', 'give', 'either', 'neither', 'nor' ,'be', 'is','so'])
    
    definitionWordTokens = set()
    for singleLemma in lemmaSet:
        try:
            wordNetDefinition = wn.synsets(singleLemma)[0].definition()
            definitionWordTokens =  definitionWordTokens.union(set(util.getNormalized_text(wordNetDefinition)))
        except:
            pass #no wordnet definitions                 
        try:
            dictionaryDefinitionDict = englishDictionary.meaning(singleLemma)            
            dictionaryDefinitionString = ""
            for key in dictionaryDefinitionDict:
                for definition in dictionaryDefinitionDict[key]:
                    dictionaryDefinitionString = dictionaryDefinitionString + " " + definition                            
            definitionWordTokens= definitionWordTokens.union(set(util.getNormalized_text(dictionaryDefinitionString)))
        except:
            pass # if no english dictionary, just use wordnet
        #END IF
        definitionWordTokens= set(definitionWordTokens).difference(trivialLowerCaseWords)
        definitionWordTokens = set([lemmatizer.lemmatize(x) for x in definitionWordTokens])
    if depth > 0:
        definitionWordTokens = definitionWordTokens.union(
            getDefiningWords(definitionWordTokens, lemmatizer,depth-1, englishDictionary))
    
    return definitionWordTokens
    
    

#===============================================================================
# 
#===============================================================================

def getWordPolarity(lemmaSet, lemmatizer, singleReview, positiveAssociationWords,
                          negativeAssociationWords,neutralWords, useDictionary = True):
    '''
    @summary: 
        1) For each qualifier word determine the polarity by looking at it's definition. If the definition does not exist, ignore
        2) if it exists, get all the words and lemmatize them. Score the number of pos, neg, and neutral words
            if preceeded by not, no, never, then score oppposite. Polarity is +/-, neutral score is seperate.
            If there is a "but", "however", then the word is conflict, simply set neutral to a negative (-1)        
    '''
    totalPolarityScore = 0
    conflict = False
    for singleLemma  in lemmaSet:
        #get the score        
        polarityScore = 0
        lemmaPolarityScore = 0        
        polarityMultiplier = 1 #is -1 if the word was negated in the sentence
        if singleLemma.startswith("-"):
            polarityMultiplier = -1
            singleLemma[1:] #ignore the "-" 
        definitionLemmatizedWordTokenSet = set()
        if useDictionary:
            definitionLemmatizedWordTokenSet = getDefiningWords(set([singleLemma]),lemmatizer, 1,None)
        definitionLemmatizedWordTokenSet.add(singleLemma)

        #now count the scores
        for singleWord in definitionLemmatizedWordTokenSet:                                               
            if singleWord in positiveAssociationWords:
                polarityScore+= 1*polarityMultiplier
            elif singleWord in negativeAssociationWords:
                polarityScore -=1*polarityMultiplier           
        #END FOR loop through the definition words of the lemma                   
        if polarityScore != 0:      
            lemmaPolarityScore = polarityScore/abs(polarityScore) # so it will be +/- 1             
        #if the polarity score is -ve for this lemma , but the total score so far is +ve, then the review is conflict
        if (lemmaPolarityScore >0 and totalPolarityScore <0) or (lemmaPolarityScore <0 and totalPolarityScore >0):
            conflict = True            
        totalPolarityScore += lemmaPolarityScore
    #END for loop through the lemmas passed into function
        
                
    ret_polarity = "neutral"
    if totalPolarityScore > 0:
        ret_polarity = "positive"
    elif totalPolarityScore < 0:
        ret_polarity = "negative"
    
    if conflict:
        ret_polarity = "conflict"
    
    return (ret_polarity,conflict, totalPolarityScore) 
                
                

        
        
        
    

#===============================================================================
# 
#===============================================================================
def unsupervisedWordNetPolarity_updateDictWithAspectPolarityPairs(allInputData, 
                        positiveAssociationWords = None, negativeAssociationWords = None, neutralWords = None,
                        useDictionary = True):
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
    polarityChangeWords = ['not', 'never', 'over', 'excess']
    lemmatizer = nltk.stem.WordNetLemmatizer()
    if positiveAssociationWords == None:
        positiveAssociationWords = ["delight","elation","excite","happiness","joy","pleasure","love","affection",
                                                    "satisfaction","contentment","relaxation","relief","calmness","politeness",
                                                    "happy",
                                                    "good", "great", "excellent","amazing","wonderful","fine", "acceptable"]
        negativeAssociationWords = ["sadness", "disappointment", "anger", "annoyance", "contempt", "irritation",
                                "anxiety", "embarrassment", "fear" , "helplessness", "powerlessness", "worry",
                                "frustration", "shame" ,"boredom", "despair", "hurt", "stress", "shock", "tension", "fear",
                                "irritation" ,"disgust"]
        neutralWords = [ "normal", "neutral", "ok", "o.k.", "okay", ]

    positiveAssociationWords = [lemmatizer.lemmatize(x,pos='a') for x in positiveAssociationWords]
    negativeAssociationWords = [lemmatizer.lemmatize(x,pos='a') for x in negativeAssociationWords]
    neutralWords = [lemmatizer.lemmatize(x) for x in neutralWords]  
    
# REMOVE ME    
#     print (positiveAssociationWords)
#     print (negativeAssociationWords)
#     print (neutralWords)
#     return
    
    #each review is a dict that contains the raw data, POS tags, DEPS (dependency parser) tags, and the 
    # actual aspects, polarity, and category for each review
    for singleReview in allInputData['sentences']['sentence']:
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
        singleReview['dictAspectPolarity'] = {} #prepare to store the results            
        for singleAspectTermDict in aspectTerms:
            aspectWord = singleAspectTermDict['@term']  
            truePolarity = singleAspectTermDict['@polarity']            
            depsLemmaList = getDependencyTaggingWordLemmas(aspectWord,singleReview,lemmatizer)
            posLemmaList = getPosTaggingWordLemmas(aspectWord,singleReview,lemmatizer) 
       
            lemmaSet = set(depsLemmaList + posLemmaList)            
            (aspectPolarity ,isconflict, polarityScore)= getWordPolarity(lemmaSet,lemmatizer,
                                                   singleReview,positiveAssociationWords,negativeAssociationWords,
                                                   neutralWords, useDictionary)                   
            singleReview['dictAspectPolarity'][aspectWord] = aspectPolarity
            
#             print("============================================================")  
#             print("SENTENCE =", singleReview['text'], "\nAspect Word =", aspectWord, " Aspect Polarity =", truePolarity)
#             print("DEPS lemmas =", depsLemmaList )
#             print("POS lemmas =", posLemmaList )
#             print("dictionary polarity = " , aspectPolarity)
    #END FOR loop through reviews
    
    for singleReview in allInputData['sentences']['sentence']:
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
        print("============================================================")  
        print("SENTENCE =", singleReview['text'])
        print("Aspects = ", singleReview['aspectTerms'])
        print("dictionary polarity = " , singleReview['dictAspectPolarity'])
        
        #output the accuracy. Since it is not a single group we are trying to detect. Precision and recall dont make
        # sense. But we can output the % of positive terms caught, % of negative, neutral and conflict
        totalPositiveTerms = 0
        totalNegativeTerms = 0
        totalNeutralTerms = 0
        totalconflictTerms = 0
        correctPositiveTerms = 0
        correctNegativeTerms = 0
        correctNeutralTerms = 0
        correctconflictTerms = 0        
        for singleReview in allInputData['sentences']['sentence']:
            #first get the aspects in the sentence        
            try:
                aspectTermsList = singleReview['aspectTerms']['aspectTerm']
            except:
                continue #no aspect terms
            
            if type(aspectTermsList) == dict:
                # if there were more than one aspect term, it would be in a list
                #this just makes the single term case (which would be a dict ) into a list of one
                # so the code is common
                aspectTermsList = [aspectTermsList]
            aspectTermsDictPolarity = singleReview['dictAspectPolarity']
            for singleAspectDict in aspectTermsList:
                aspectWord = singleAspectDict['@term']  
                truePolarity = singleAspectDict['@polarity']
                if truePolarity == "positive":
                    totalPositiveTerms+=1
                elif truePolarity == "negative":
                    totalNegativeTerms+=1
                elif truePolarity == "neutral":
                    totalNeutralTerms+=1
                elif truePolarity == "conflict":
                    totalconflictTerms+=1                                        
                try:
                    dictPolarity = aspectTermsDictPolarity[aspectWord]
                    if dictPolarity == truePolarity:
                        if truePolarity == "positive":
                            correctPositiveTerms+=1
                        elif truePolarity == "negative":
                            correctNegativeTerms+=1
                        elif truePolarity == "neutral":
                            correctNeutralTerms+=1
                        elif truePolarity == "conflict":
                            correctconflictTerms+=1                             
                except:
                    pass#this was a failed case, ignore
        #end for loop through all the reviews
        
    if totalPositiveTerms != 0:
        print("Positive cases" , totalPositiveTerms, correctPositiveTerms, 
                                                correctPositiveTerms/totalPositiveTerms)
    if totalNegativeTerms != 0:
        print("Negative cases", totalNegativeTerms, correctNegativeTerms,
                                                correctNegativeTerms/totalNegativeTerms)
    if totalNeutralTerms != 0:
        print("Neutral cases" , totalNeutralTerms, correctNeutralTerms,
                                                    correctNeutralTerms/totalNeutralTerms)
    if totalconflictTerms != 0:
        print("Conflict cases", totalconflictTerms, correctconflictTerms,
                                                    correctconflictTerms/totalconflictTerms)
        
    print ("total success", (correctPositiveTerms+correctNegativeTerms+correctNeutralTerms+correctconflictTerms)/
                                            (totalconflictTerms+totalNegativeTerms+totalNeutralTerms+totalPositiveTerms) )
              
#==========================================================
# 
#==========================================================
def supervisedWordNetPolarity_updateDictWithAspectPolarityPairs(trainData, testData):    
    '''
    '''        
    positiveWordAssocList = []
    negativeWordAssocList = []
    neutralWordAssocList = []
    #If an aspect has a polarity and NOT conflict
    #do the same lemma detection, and save it as positive or negative or neutral.
    #then run the test data with the updated pos, negative, neutral words as unsupervised learning
    
    #each review is a dict that contains the raw data, POS tags, DEPS (dependency parser) tags, and the 
    # actual aspects, polarity, and category for each review
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for singleReview in trainData['sentences']['sentence']:
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
            lemmaSet = set(depsLemmaList + posLemmaList)    
            #we know the polarity, store it in the right list (except for conflicts)
            storageList = []            
            if truePolarity == "positive":
                storageList = positiveWordAssocList
            elif truePolarity == "negative":
                storageList = negativeWordAssocList
            elif truePolarity == "neutral":
                storageList = neutralWordAssocList
            for singleWord in lemmaSet:
                storageList.append(singleWord)
        #END FOR LOOP through a single review
    #END FOR loop through all reviews
    #At this point we have the word association lists from the training data, now test it on the test data
    unsupervisedWordNetPolarity_updateDictWithAspectPolarityPairs(testData, list(set(positiveWordAssocList)),
                                                                  list(set(negativeWordAssocList)), list(set(neutralWordAssocList)),
                                                                  useDictionary = False) 
        
    print("done with supervised word polarity detection")
                    
#===========================================================
# 
#===========================================================

def unsupervisedDetectConflictSentences(allDataDict, conflictDetectionWords = None):
    '''
        This uses a list of frequent conflict indicator words like [ ' but' , 'however', 'still', 'nonetheless']
    '''
    
    if conflictDetectionWords == None:
        conflictDetectionWords = [ 'but' , ' but' , ',but' , 'however', ' however', ',however', 'still', ' still', ',still', 
                                  'nonetheless',' nonetheless' , ',nonetheless', 'nevertheless', ' nevertheless', ',nevertheless', 
                                  'though' ,' though' ,',though' , 'although' , ' although' , ',although']

    for singleReview in allDataDict['sentences']['sentence']:
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
        singleReview['dictAspectPolarity'] = {} #prepare to store the results            
        for singleAspectTermDict in aspectTerms:
            aspectWord = singleAspectTermDict['@term']  
            truePolarity = singleAspectTermDict['@polarity']
            allLemmas = []            
            allLemmaSentences = singleReview['DEPStagging']
            

            
            for singleSentence in allLemmaSentences:
                allLemmas = allLemmas + [x['word'] for x in singleSentence[1:]]
       
            aspectPolarity = "neutral"
            
            if truePolarity == "conflict":
                lemmaSet = set(allLemmas)            
                for singleLemma in lemmaSet:
                    if singleLemma in conflictDetectionWords:
                        aspectPolarity = "conflict"
                                        
            singleReview['dictAspectPolarity'][aspectWord] = aspectPolarity
            
            print("============================================================")  
            print("SENTENCE =", singleReview['text'], "\nAspect Word =", aspectWord, " Aspect Polarity =", truePolarity)
            print("dictionary polarity = " , aspectPolarity)
    #END FOR loop through reviews
    
    for singleReview in allDataDict['sentences']['sentence']: 
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
        print("============================================================")  
        print("SENTENCE =", singleReview['text'])
        print("Aspects = ", singleReview['aspectTerms'])
        print("dictionary polarity = " , singleReview['dictAspectPolarity'])
        
    #output the accuracy. Since it is not a single group we are trying to detect. Precision and recall dont make
    # sense. But we can output the % of positive terms caught, % of negative, neutral and conflict    
    totalNeutralTerms = 0
    totalconflictTerms = 0
    correctNeutralTerms = 0
    correctconflictTerms = 0        
    for singleReview in allDataDict['sentences']['sentence']:
        #first get the aspects in the sentence        
        try:
            aspectTermsList = singleReview['aspectTerms']['aspectTerm']
        except:
            continue #no aspect terms
        
        if type(aspectTermsList) == dict:
            # if there were more than one aspect term, it would be in a list
            #this just makes the single term case (which would be a dict ) into a list of one
            # so the code is common
            aspectTermsList = [aspectTermsList]
        aspectTermsDictPolarity = singleReview['dictAspectPolarity']
        for singleAspectDict in aspectTermsList:
            aspectWord = singleAspectDict['@term']  
            truePolarity = singleAspectDict['@polarity']
            if truePolarity == "neutral":
                totalNeutralTerms+=1
            elif truePolarity == "conflict":
                totalconflictTerms+=1                                        
            try:
                dictPolarity = aspectTermsDictPolarity[aspectWord]
                if dictPolarity == truePolarity:
                    if truePolarity == "neutral":
                        correctNeutralTerms+=1
                    elif truePolarity == "conflict":
                        correctconflictTerms+=1                             
            except:
                pass#this was a failed case, ignore
    #end for loop through all the reviews
    

    if totalNeutralTerms != 0:
        print("Neutral cases" , totalNeutralTerms, correctNeutralTerms,
                                                    correctNeutralTerms/totalNeutralTerms)
    if totalconflictTerms != 0:
        print("Conflict cases", totalconflictTerms, correctconflictTerms,
                                                    correctconflictTerms/totalconflictTerms)
        
    print ("total success", (correctNeutralTerms+correctconflictTerms)/
                                            (totalNeutralTerms+totalconflictTerms) )
        
#===============================================================================
# 
#===============================================================================

def supervisedDetectConflictSentences( trainData, testData):
    '''
    '''

#     if conflictDetectionWords == None:
#         conflictDetectionWords = [ ' but' , 'however', 'still', 'nonetheless', ' nevertheless']
# 
#         for singleReview in allDataDict['sentences']['sentence']:
#         #first get the aspects in the sentence        
#         try:
#             aspectTerms = singleReview['aspectTerms']['aspectTerm']
#         except:
#             continue #no aspect terms
#         
#         if type(aspectTerms) == dict:
#             # if there were more than one aspect term, it would be in a list
#             #this just makes the single term case (which would be a dict ) into a list of one
#             # so the code is common
#             aspectTerms = [aspectTerms]
#         singleReview['dictAspectPolarity'] = {} #prepare to store the results            
#         for singleAspectTermDict in aspectTerms:
#             aspectWord = singleAspectTermDict['@term']  
#             truePolarity = singleAspectTermDict['@polarity']
#             allLemmas = []            
#             allLemmaSentences = singleReview['DEPStagging']
#             for singleSentence in allLemmaSentences:
#                 allLemmas = allLemmas + [x['word'] for x in singleSentence[1:]]
#        
#             lemmaSet = set(allLemmas)            
#             (aspectPolarity ,isconflict, polarityScore)= getWordPolarity(lemmaSet,lemmatizer,
#                                                    singleReview,positiveAssociationWords,negativeAssociationWords,
#                                                    neutralWords, useDictionary)                   
#             singleReview['dictAspectPolarity'][aspectWord] = aspectPolarity
#             
#             print("============================================================")  
#             print("SENTENCE =", singleReview['text'], "\nAspect Word =", aspectWord, " Aspect Polarity =", truePolarity)
#             print("DEPS lemmas =", depsLemmaList )
#             print("POS lemmas =", posLemmaList )
#             print("dictionary polarity = " , aspectPolarity)
#     #END FOR loop through reviews
#     
#     for singleReview in allInputData['sentences']['sentence']:
#     #first get the aspects in the sentence        
#         try:
#             aspectTerms = singleReview['aspectTerms']['aspectTerm']
#         except:
#             continue #no aspect terms
#         
#         if type(aspectTerms) == dict:
#             # if there were more than one aspect term, it would be in a list
#             #this just makes the single term case (which would be a dict ) into a list of one
#             # so the code is common
#             aspectTerms = [aspectTerms]
#         print("============================================================")  
#         print("SENTENCE =", singleReview['text'])
#         print("Aspects = ", singleReview['aspectTerms'])
#         print("dictionary polarity = " , singleReview['dictAspectPolarity'])
#         
#         #output the accuracy. Since it is not a single group we are trying to detect. Precision and recall dont make
#         # sense. But we can output the % of positive terms caught, % of negative, neutral and conflict
#         totalPositiveTerms = 0
#         totalNegativeTerms = 0
#         totalNeutralTerms = 0
#         totalconflictTerms = 0
#         correctPositiveTerms = 0
#         correctNegativeTerms = 0
#         correctNeutralTerms = 0
#         correctconflictTerms = 0        
#         for singleReview in allInputData['sentences']['sentence']:
#             #first get the aspects in the sentence        
#             try:
#                 aspectTermsList = singleReview['aspectTerms']['aspectTerm']
#             except:
#                 continue #no aspect terms
#             
#             if type(aspectTermsList) == dict:
#                 # if there were more than one aspect term, it would be in a list
#                 #this just makes the single term case (which would be a dict ) into a list of one
#                 # so the code is common
#                 aspectTermsList = [aspectTermsList]
#             aspectTermsDictPolarity = singleReview['dictAspectPolarity']
#             for singleAspectDict in aspectTermsList:
#                 aspectWord = singleAspectDict['@term']  
#                 truePolarity = singleAspectDict['@polarity']
#                 if truePolarity == "positive":
#                     totalPositiveTerms+=1
#                 elif truePolarity == "negative":
#                     totalNegativeTerms+=1
#                 elif truePolarity == "neutral":
#                     totalNeutralTerms+=1
#                 elif truePolarity == "conflict":
#                     totalconflictTerms+=1                                        
#                 try:
#                     dictPolarity = aspectTermsDictPolarity[aspectWord]
#                     if dictPolarity == truePolarity:
#                         if truePolarity == "positive":
#                             correctPositiveTerms+=1
#                         elif truePolarity == "negative":
#                             correctNegativeTerms+=1
#                         elif truePolarity == "neutral":
#                             correctNeutralTerms+=1
#                         elif truePolarity == "conflict":
#                             correctconflictTerms+=1                             
#                 except:
#                     pass#this was a failed case, ignore
#         #end for loop through all the reviews
#         
#         if totalPositiveTerms != 0:
#             print("Positive cases" , totalPositiveTerms, correctPositiveTerms, 
#                                                     correctPositiveTerms/totalPositiveTerms)
#         if totalNegativeTerms != 0:
#             print("Negative cases", totalNegativeTerms, correctNegativeTerms,
#                                                     correctNegativeTerms/totalNegativeTerms)
#         if totalNeutralTerms != 0:
#             print("Neutral cases" , totalNeutralTerms, correctNeutralTerms,
#                                                         correctNeutralTerms/totalNeutralTerms)
#         if totalconflictTerms != 0:
#             print("Conflict cases", totalconflictTerms, correctconflictTerms,
#                                                         correctconflictTerms/totalconflictTerms)
#             
#         print ("total success", (correctPositiveTerms+correctNegativeTerms+correctNeutralTerms+correctconflictTerms)/
#                                                 (totalconflictTerms+totalNegativeTerms+totalNeutralTerms+totalPositiveTerms) )
#         
