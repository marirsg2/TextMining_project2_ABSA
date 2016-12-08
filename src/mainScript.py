'''
Created on Nov 20, 2016

@author: marir
'''
import copy


from config_parser import pickleFile, pickleFolder
import nltkWordnetAspectExtraction as lexicalApproach
import file_operations
import doc2VecAspectIdentification as d2v 
from from_train import FromTrain



(restaurantTrainDict,restaurantTestDict,laptopTrainDict, laptopTestDict) = \
                                file_operations.loadAndGetRawDataFromPickle(pickleFolder, pickleFile)
#at this point you have all your training and test data in python dictionaries. Run algorithms


#===============================================================================
#   Using doc 2 vector to get a list of aspects
#===============================================================================
allRestaurantData = copy.deepcopy(restaurantTrainDict)
allRestaurantData['sentences']['sentence'] = allRestaurantData['sentences']['sentence'] + restaurantTestDict['sentences']['sentence']
allLaptopData = copy.deepcopy(laptopTrainDict)
allLaptopData ['sentences']['sentence'] = allLaptopData['sentences']['sentence'] + laptopTestDict['sentences']['sentence']

#===============================================================================
#modified at Mon Nov 28 01:10:36 2016
#allLaptopData.update(laptopTestDict) 
#The update sentence should be deleted or use append like function
#otherwise the data set will be ONLY the testdict
#===============================================================================

#from_train = FromTrain(allRestaurantData)
#from_train = FromTrain(allLaptopData)
from_train = FromTrain(laptopTrainDict)
#aspects = from_train.extract_aspects()
res = from_train.aspects_performance(laptopTestDict)
#res = from_train.aspects_performance(laptopTrainDict)
#res = from_train.aspects_performance(allLaptopData)
#res = from_train.aspects_performance(allLaptopData)
print (res)
adjs = from_train.get_adj_polarity()
pairs = from_train.get_pair_polarity()
#print (adjs)
#print (pairs)
#aspects = from_train.aspects_possibility()

# list_doc2vecExtractedAspects = d2v.getListOfAspects({'laptop':allLaptopData , 'restaurant' : allRestaurantData}) 
# print (list_doc2vecExtractedAspects)


#===============================================================================
#                USING LEXICAL DEFINITION TO FIND ASPECTS 
#   This approach failed, the commented code is kept here for historical tracking, and if we need to try
#   this technique again.
#===============================================================================
#code to use nltk and wordnet lexical dictionary to identify the aspects from the reviews
# allRestaurantData = copy.deepcopy(restaurantTrainDict)
# allRestaurantData.update(restaurantTestDict)
# allLaptopData = copy.deepcopy(laptopTrainDict)
# allLaptopData.update(laptopTestDict)
# lexicalApproach.nltkWordnetAspectExtraction([allRestaurantData,allLaptopData], ['restaurant', 'laptop'])



