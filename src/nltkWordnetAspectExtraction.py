'''
Created on Nov 22, 2016

@author: srg315
'''
import nltk
from nltk.corpus import wordnet as wn


'''
    NOTE: This approach was abandoned as the initial results showed that the wordnet relationships
    was incomplete and had a lot of holes.
'''

'''
    This approach uses the following ideas
    1) The category is given: Restaurant and Laptop
    2) Assumption : In most reviews there is atleast one aspect associated with the category
             The aspect maybe a noun, or an adjective and we have to infer the noun (eg: Expensive -> price)
    3) This approach is primarily to see if the nouns in the review are related to the category. The relationships are
    found using wordnet definitions.
    
    FOR explanations on the different relationships in wordnet:
    http://trimc-nlp.blogspot.com/2015/06/python-nltk-and-wordnet.html
    
'''

def nltkWordnetAspectExtraction(listOfReviewDataDicts, listOfCategories):
    '''
    @param listOfCategories: The categories are input as wordnet synset, not just plain english. 
    @summary: For each set of reviews (in one dictionary), and the category found at the same index
    in the listOfCategories, we apply the following approach
    1) Get the definition from wordnet
    2) For each noun in each review , lemmatize it and check the wordnet definition. 
            a) If there are nouns in common with the category definition, then it is a candidate aspect
            b) If the noun is hypernym or holonym of the category, then the adjective qualifying it 
            will decide the aspect. eg: Expensive cafeteria -> Price. This can be through Pertainyms or
            from the definition of the qualifying adjective, we can extract the noun. 
    '''
    for idx in range(0,len(listOfCategories)):
        currentReviewsDict = listOfReviewDataDicts[idx]
        currentCategory = listOfCategories[idx]        
        categoryLexicalDefinition = wn.synsets(currentCategory)
        print (categoryLexicalDefinition)
        print (categoryLexicalDefinition[0].definition())
        '''
Pertainyms
Adjectives that are derived from Nouns. eg: Criminal -> Crime
        '''
#===============================================================================
# 
#===============================================================================

if __name__ == "__main__":
    a = wn.synsets('laptops')
    #most of the relationships are empty lists, and the definition is very sparse, and the relationships of those
    # worse in the definition were also weak. This was the same for restaurants as well. So we abandoned this
    # approach
    print(a)
    for piece in a[:1]:
        print ("=================================================")
        print (piece.definition())
        print (piece.hypernyms())
        print (piece.hyponyms())
        print (piece.meronyms())             
        print (piece.topic_domains())
        
    '''
    antonyms
hypernyms, instance_hypernyms
hyponyms, instance_hyponyms
member_holonyms, substance_holonyms, part_holonyms
member_meronyms, substance_meronyms, part_meronyms
topic_domains, region_domains, usage_domains
attributes
derivationally_related_forms
entailments
causes
also_sees
verb_groups
similar_tos
pertainyms
    '''