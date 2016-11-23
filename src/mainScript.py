'''
Created on Nov 20, 2016

@author: marir
'''
import copy
import pickle

from preProcess import pickleFile, pickleFolder
import nltkWordnetAspectExtraction as lexicalApproach


#load the  reviews dictionary x4 for restaurant train, test and laptop train , test
restaurantTrainDict = {}
restaurantTestDict = {}
laptopTrainDict = {}
laptopTestDict = {}
with open(pickleFolder+pickleFile,'rb') as pickleSource:
    restaurantTrainDict = pickle.load(pickleSource)
    restaurantTestDict = pickle.load(pickleSource)
    laptopTrainDict = pickle.load(pickleSource)
    laptopTestDict = pickle.load(pickleSource)

print ("all data loaded in python dicts")
#at this point you have all your training and test data in python dictionaries. Run algorithms

#code to use nltk and wordnet lexical dictionary to identify the aspects from the reviews
allRestaurantData = copy.deepcopy(restaurantTrainDict)
allRestaurantData.update(restaurantTestDict)
allLaptopData = copy.deepcopy(laptopTrainDict)
allLaptopData.update(laptopTestDict)
lexicalApproach.nltkWordnetAspectExtraction([allRestaurantData,allLaptopData], ['restaurant', 'laptop'])



