'''
Created on Nov 20, 2016

@author: marir
'''
import copy

from config_parser import pickleFile, pickleFolder
import doc2VecAspectIdentification
import doc2VecAspectIdentification as d2v 
import file_operations
from from_train import FromTrain
import nltkWordnetAspectExtraction as lexicalApproach
import wordNetAspectPolarityDetection


#IMPORTANT: please run preProcess.py before the main script. Ensure you update the location of the 
# stanford dependency parser and  the POS tagger
(restaurantTrainDict,restaurantTestDict,laptopTrainDict, laptopTestDict) = \
                                file_operations.loadAndGetRawDataFromPickle(pickleFolder, pickleFile)
#at this point you have all your training and test data in python dictionaries. Run algorithms


allRestaurantData = copy.deepcopy(restaurantTrainDict)
allRestaurantData['sentences']['sentence'] = allRestaurantData['sentences']['sentence'] + restaurantTestDict['sentences']['sentence']
allLaptopData = copy.deepcopy(laptopTrainDict)
allLaptopData ['sentences']['sentence'] = allLaptopData['sentences']['sentence'] + laptopTestDict['sentences']['sentence']

#================ TASK 1  - ASPECT IDENTIFICATION  ============================================
'''
    The best results for usupervised in task 1 was from the frequency approach.
    The supervised approach (With training data) obviously performed better
'''

#---------UNSUPERVISED TECHNIQUES-------------

#1) Doc 2 Vec (improvement on word 2 vector for training documents with labels)
#The doc2vec approach has been commented out because you need to first install gensim library
#also uncomment the import line
# doc2VecResults = \
#         doc2VecAspectIdentification.getDictionaryOfAspectsByCategory({"laptop":allLaptopData,"restaurant":allRestaurantData})
#print (doc2VecResults)

#-----------------------------------------------

#2) wordNet definitions relationships for aspect identifications
#This approach tried to identify aspects by finding nouns that were in the definitions of words that were related to the review
# main categories, namely "laptop" and "restaurant". This failed because there definitions, synonyms, meronyms (part relationships)
# were incomplete or sparse in wordnet. The script is nltkWordnetAspectExtraction.py

#-----------------------------------------------

#3) Frequency based approach

#---------------------SUPERVISED TRAINING-------------------------


#===================================================================================
#from_train = FromTrain(allLaptopData)
#from_train = FromTrain(laptopTrainDict)
#aspects = from_train.extract_aspects()
#res = from_train.aspects_performance(laptopTestDict)
#res = from_train.aspects_performance(laptopTrainDict)
#res = from_train.aspects_performance(allLaptopData)
#res = from_train.aspects_performance(allLaptopData)
# res = from_train.get_pair_polarity()
# for r in res:
#     print (r)
    
#==========================TASK2 ASPECT POLARITY==================================

#-------- UNSUPERVISED APPROACHES---------------
# 1) Wordnet aspect polarity detection  ( in wordNetAspectPolarityDetection.py)
'''This approach seeks to find the polarity by counting the number of seed words which define positive, negative, and
neutral adjectives. These seed words were collected from unsupervised data (list of common human emotions) or
supervised data (from the training data). Note we did not train a model in this step, we just collected positive, negative,
and neutral words. 
NOTE: Conflict detection has a seperate function and uses a list of words to detect conflict, like ["but", however, although.]
'''
#The result is printed out from the functions themselves
print("=========Results for task 2 in LAPTOP category   by UNsupervised wordnet definitions for polarity detection==========")
wordNetAspectPolarityDetection.unsupervisedWordNetPolarity_updateDictWithAspectPolarityPairs(allLaptopData)
print("=========Results for task 2 in  RESTAURANT category   by UNunsupervised wordnet definitions for polarity detection==========")
wordNetAspectPolarityDetection.unsupervisedWordNetPolarity_updateDictWithAspectPolarityPairs(allRestaurantData)
print("=========Results for task 2 in LAPTOP category   by SUPERVISED wordnet definitions for polarity detection==========")
wordNetAspectPolarityDetection.supervisedWordNetPolarity_updateDictWithAspectPolarityPairs(laptopTrainDict,laptopTestDict)
print("=========Results for task 2 in RESTAURANT category   by SUPERVISED wordnet definitions for polarity detection==========")
wordNetAspectPolarityDetection.supervisedWordNetPolarity_updateDictWithAspectPolarityPairs(restaurantTrainDict,restaurantTestDict)
print("=========Results for task 2 in LAPTOP category  for CONFLICT detection (UNSUPERVISED)==========")
wordNetAspectPolarityDetection.unsupervisedDetectConflictSentences(allLaptopData)
print("=========Results for task 2 in RESTAURANT category   for CONFLICT detection (UNSUPERVISED)==========")
wordNetAspectPolarityDetection.unsupervisedDetectConflictSentences(allRestaurantData)
print("=============x-------------------END RESULTS FOR UNSUPERVISED TASK 2--------------x===============================")

#----------------------- SUPERVISED approach to task 2
