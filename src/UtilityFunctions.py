'''
Created on Nov 18, 2016

@author: Zhen Song Ram
'''

import pickle
import os

#===============================================================================
# 
#===============================================================================

def pickleListOfObjects(pickleFolder, pickleFileName, listOfObjects):
    '''
    @summary: Self explanatory. NOTE: if the folder is a relative path, note that it should be relative to this file
    @todo: Improve this to allow file appends and such
    '''

    if not os.path.exists(pickleFolder):
        os.makedirs(pickleFolder)
    
    if os.path.exists(pickleFileName):
        os.remove(pickleFileName)
    
    with open(pickleFolder+pickleFileName,'wb') as pickleFile:
        for singleObject in listOfObjects:
            pickle.dump(singleObject,pickleFile)