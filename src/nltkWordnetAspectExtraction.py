'''
Created on Nov 22, 2016

@author: marir
'''


'''
    This approach uses the following ideas
    1) The category is given: Restaurant and Laptop
    2) Assumption : In each review there is atleast one aspect associated with the category
             The aspect maybe a noun, or an adjective and we have to infer the noun (eg: Expensive -> price)
    3) This approach is primarily to see if the nouns in the review are related to the category using wordnet
    definitions.
    4) The adjective mapping needs to be done with another method
'''

def nltkWordnetAspectExtraction(listOfReviewDataDicts, listOfCategories):
    '''
    
    '''
    pass