'''
Created on Nov 20, 2016

@author: marir
'''
import copy


from preProcess import pickleFile, pickleFolder
import nltkWordnetAspectExtraction as lexicalApproach
import FileOperations



(restaurantTrainDict,restaurantTestDict,laptopTrainDict, laptopTestDict) = \
                                FileOperations.loadAndGetRawDataFromPickle(pickleFolder, pickleFile)
#at this point you have all your training and test data in python dictionaries. Run algorithms




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



