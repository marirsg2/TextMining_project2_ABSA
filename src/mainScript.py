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
#import evaluation_task1_freq_tfidf as eval


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
'''The doc2vec approach has been commented out because you need to first install gensim library
also uncomment the import line. See the script for a detailed description'''
# doc2VecResults = \
#         doc2VecAspectIdentification.getDictionaryOfAspectsByCategory({"laptop":allLaptopData,"restaurant":allRestaurantData})
#print (doc2VecResults)

#-----------------------------------------------

#2) wordNet definitions relationships for aspect identifications
'''
This approach tried to identify aspects by finding nouns that were in the definitions of words that were related to the review
 main categories, namely "laptop" and "restaurant". This failed because there definitions, synonyms, meronyms (part relationships)
 were incomplete or sparse in wordnet. The script is nltkWordnetAspectExtraction.py
 '''

#-----------------------------------------------

#3) Frequency based approach

#---------------------SUPERVISED TRAINING-------------------------

supervised_laptopTrain = FromTrain(laptopTrainDict)
supervised_restaurantTrain = FromTrain(restaurantTrainDict)
#need py 3.5 to run this function. If not, for results see writeup
#Also uncomment the import of evaluation_task1_freq_tfidf 
#eval.evaluate2();

print("==========================TASK2 ASPECT POLARITY==================================")

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

print("----------------------- SUPERVISED approach to task 2-----------------------------")
'''
These results were actually really low because we used the dependency parser to extract the nouns 
and their adjectives for polarity. Only if the noun matched the aspect, then we would save the nouns, 
adjective and the polarity (from the review data). 
The dependency parser  did not detect a majority of the aspects correctly. So our training model was weak.
IMPROVEMENT: If we don't try and extract the aspects with the dependency parser, and instead we can
 just take the aspects directly. This would make the model stronger as it would have all the aspects

'''
#get the noun adj pair prediction for the training data
laptop_listOfNounAdjPairs = supervised_laptopTrain.get_pair_polarity();
restaurant_listOfNounAdjPairs = supervised_restaurantTrain.get_pair_polarity();
#compare with the results from the test data
#first get the test data results
test_laptopTrain = FromTrain(laptopTestDict)
test_restaurantTrain = FromTrain(restaurantTestDict)
laptop_testResultsNounAdjPairs = test_laptopTrain.get_pair_polarity();
restaurant_testResultsNounAdjPairs = test_restaurantTrain.get_pair_polarity();
#now compare with the train data results
print("=====TASK 2- supervised training results for LAPTOP reviews==========")


trained_list_laptop = supervised_laptopTrain.get_aspect_polarity()

test_laptopTrain.getAccuracy(trained_list_laptop, laptopTestDict)

print("=====TASK 2- supervised training results for RESTAURANT reviews==========")

trained_list_restaurant = supervised_restaurantTrain.get_aspect_polarity()

test_restaurantTrain.getAccuracy(trained_list_restaurant, restaurantTestDict)


