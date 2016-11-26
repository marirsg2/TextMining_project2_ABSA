'''
Created on Nov 25, 2016

@author: marir
'''


import random
import gensim
from gensim.models import Doc2Vec 
from gensim.models.doc2vec import TaggedDocument



assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow otherwise"


#code borrowed from 
# https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/doc2vec-IMDB.ipynb
def getNormalized_text(text):
    norm_text = text.lower()
    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')
    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        norm_text = norm_text.replace(char, ' ')
    return norm_text.split()


#===============================================================================
# 
#===============================================================================

def getTaggedDocumentsWithNormalizedText (list_categoryAndReviewsTuple):
    ret_list_taggedDocuments = []
    for entry in list_categoryAndReviewsTuple:
        list_allReviewsInCategory = [x['text'] for x in entry[1]['sentences']['sentence'] ]        
        for rawReviewText in list_allReviewsInCategory:
            ret_list_taggedDocuments.append( TaggedDocument( words = getNormalized_text(rawReviewText) , tags = [ entry[0] ] ) )
    
    return ret_list_taggedDocuments

#===============================================================================
# 
#===============================================================================

def getTaggedDocumentsWithNounsOnly (list_categoryAndReviewsTuple):
    ret_list_taggedDocuments = []
    for entry in list_categoryAndReviewsTuple:
        list_filteredPOSreviews = []
        list_allReviewsInCategoryAsPOStext= [x['POStaggedText'] for x in entry[1]['sentences']['sentence'] ];
        for singlePOStaggedReview in list_allReviewsInCategoryAsPOStext:
            filteredSentence = []
            for singleTag in singlePOStaggedReview:
                if singleTag[1] in ["NN", "NNS", "JJ", "JJS"]:
                    filteredSentence.append(singleTag[0])
            list_filteredPOSreviews.append(filteredSentence)            
        for filteredPOSreview in list_filteredPOSreviews:
            ret_list_taggedDocuments.append( TaggedDocument( words = filteredPOSreview , tags = [ entry[0] ] ) )
    
    return ret_list_taggedDocuments


#===============================================================================
# 
#===============================================================================
def getListOfAspects(dictOfReviewsByCategory):
    '''
    
    @param dictOfReviewsByCategory: This is a list of dicts. the keys are the categories, and the values are the dicts
    that contain the reviews. Note that the reviews are stored as a dict which contains the raw data, pos tagged data, and the correct
    aspects for each review 
    @summary: This function uses doc 2 vec to train vector representations for every word in the review  with the category
    label that the review is associated with. This function also uses two random news articles from unrelated categories
    so that only strongly connected aspects will be similar to the categories that they came from. 
    '''
    
    #need another 2 corpus of roughly 3k each
    
    # First train two doc 2 vec categories  
    list_categoryAndReviewsTuple = dictOfReviewsByCategory.items()

#     list_taggedDocuments = getTaggedDocumentsWithNormalizedText(list_categoryAndReviewsTuple)
    list_taggedDocuments = getTaggedDocumentsWithNounsOnly(list_categoryAndReviewsTuple)

    #Now when we train the data we need to randomize it since the learning rate reduces over iterations
    randomizedData = []
    while len(list_taggedDocuments) > 0:
        selection = random.choice(list_taggedDocuments)
        randomizedData.append(selection)
        list_taggedDocuments.remove(selection) 
    
    #hierarchical sampling is turned off (hs = 0)
    d2vModel = Doc2Vec(documents=randomizedData, size = 200 , alpha= 0.1, window = 10, min_count= 2, workers=6, hs=0, iter =1000)
    print (d2vModel.most_similar("laptop", topn=20))
    print("=========================================")
    print (d2vModel.most_similar("restaurant", topn=20))
    print (len(d2vModel.vocab))
    