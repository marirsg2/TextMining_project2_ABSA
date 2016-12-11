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

from_train = FromTrain(allLaptopData)
#from_train = FromTrain(laptopTrainDict)
#aspects = from_train.extract_aspects()
#res = from_train.aspects_performance(laptopTestDict)
#res = from_train.aspects_performance(laptopTrainDict)
#res = from_train.aspects_performance(allLaptopData)
#res = from_train.aspects_performance(allLaptopData)
res = from_train.get_pair_polarity()
for r in res:
    print (r)



