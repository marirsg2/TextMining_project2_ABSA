'''
Created on Nov 25, 2016

@author: marir
'''


import random
import gensim
from gensim.models import Doc2Vec 
from gensim.models.doc2vec import TaggedDocument

assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow otherwise"

'''
    NOTE: This approach was abandoned as the initial results showed that the similarity between
    words we expected to have strong relationships, like laptop and battery , was very weak.
    We also saw relationships between restaurant and hard-drive. The issue is lack of diversity and
    quantity of data. We also think we could have improved the results by only training on the nouns
    and adjectives
    
    the main function for this script is the last function getListOfAspects()
'''


'''
'''


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
            sentenceInput =  getNormalized_text(rawReviewText)
            sentenceInput.insert(0,entry[0] )
            sentenceInput.insert(int(len(sentenceInput)/2),entry[0] )
            sentenceInput.insert(len(sentenceInput),entry[0] )
            ret_list_taggedDocuments.append( TaggedDocument( words = sentenceInput , tags = [ entry[0] ] ) )
    
    return ret_list_taggedDocuments
#===============================================================================
# 
#===============================================================================

def getTaggedDocumentsWithDEPSnounsOnly (list_categoryAndReviewsTuple):
    ret_list_taggedDocuments = []
    for entry in list_categoryAndReviewsTuple:
        list_filteredDEPSreviews = []
        list_allReviewsInCategoryAsDEPStext= [x['DEPStagging'] for x in entry[1]['sentences']['sentence'] ];
        for singleDEPStaggedReview in list_allReviewsInCategoryAsDEPStext:            
            filteredSentence = []            
            for singleTag in singleDEPStaggedReview:
                if singleTag['tag'] in ["NN", "NNS"] and singleTag['word'] not in ["laptop","restaurant"]:#, "JJ", "JJS"]:
                    filteredSentence.append(singleTag['word'])                
#             filteredSentence.insert(0,entry[0] )
#             filteredSentence.insert(int(len(filteredSentence)/2),entry[0] )
            filteredSentence.insert(len(filteredSentence)-1,entry[0] )
            list_filteredDEPSreviews.append(filteredSentence)            
        for filteredDEPSreview in list_filteredDEPSreviews:
            ret_list_taggedDocuments.append( TaggedDocument( words = filteredDEPSreview , tags = [ entry[0] ] ) )
    
    return ret_list_taggedDocuments

#===============================================================================
# 
#===============================================================================

def getTaggedDocumentsWithPOSnounsOnly (list_categoryAndReviewsTuple):
    ret_list_taggedDocuments = []
    for entry in list_categoryAndReviewsTuple:
        list_filteredPOSreviews = []
        list_allReviewsInCategoryAsPOStext= [x['POStaggedText'] for x in entry[1]['sentences']['sentence'] ];
        for singlePOStaggedReview in list_allReviewsInCategoryAsPOStext:            
            for singleSentence in singlePOStaggedReview:
                filteredSentence = []
                for singleTag in singleSentence:
                    if singleTag[1] in ["NN", "NNS"] and singleTag[0] not in ["laptop","restaurant"]:#, "JJ", "JJS"]:
                        filteredSentence.append(singleTag[0])                
                filteredSentence.insert(0,entry[0] )
                filteredSentence.insert(int(len(filteredSentence)/2),entry[0] )
                filteredSentence.insert(len(filteredSentence),entry[0] )
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
    list_taggedDocuments = getTaggedDocumentsWithDEPSnounsOnly(list_categoryAndReviewsTuple)

    #Now when we train the data we need to randomize it since the learning rate reduces over iterations
    randomizedData = []
    while len(list_taggedDocuments) > 0:
        selection = random.choice(list_taggedDocuments)
        randomizedData.append(selection)
        list_taggedDocuments.remove(selection) 
    
    #hierarchical sampling is turned off (hs = 0)
    d2vModel = Doc2Vec(documents=randomizedData, size = 100 , alpha= 0.01,
                        window = 3, min_count= 2, workers=6, hs=0, iter =1000)
    print("For laptop")
    print (d2vModel.most_similar("laptop", topn=20))
    print("=========================================")
    print("For restaurant")
    print (d2vModel.most_similar("restaurant", topn=20))
    print (len(d2vModel.vocab))
    