from FileOperations import FileOperations
import os
from nltk.tag.stanford import StanfordPOSTagger
import json
from os import listdir
from os.path import isfile, join
import shutil
import UtilityFunctions

tagedDataPath = '../taged-data/'
pickleFolder = '../PickledData/'
pickleFile = 'preProcessedData.p'

def getReviewDictWithTagging():
    file_name = "../data/Restaurants_Train.xml"

    os.environ['CLASSPATH']="../stanford_postagger/stanford-postagger.jar"
    os.environ['STANFORD_MODELS']='../stanford_postagger/models/english-left3words-distsim.tagger'
    os.environ['JAVAHOME']= "C:\\Program Files\\Java\jre1.8.0_71\\bin"    

    st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
    fo = FileOperations(file_name)
#     fo.get_xml()
#     sentences = fo.get_sentences()

#     f = open('../taged-data' + file_name[7:-4] + '.json', 'a')
#     cur = 0
#     for line in sentences:
#         cur += 1
#         print (cur, cur * 100 / len(sentences), '%')
#         res = st.tag(line.split())
#         json_tag = json.dumps(res)
#         f.write(json_tag)
#         f.write('\n')
#     f.close()
    
    #this is a much easier way to convert an xml file directly to a dictionary in python to access data.
    reviewsDict = fo.convertXmlToDict()
    allReviews = reviewsDict['sentences']['sentence']
    allTexts = [x['text'].split() for x in allReviews]
    allTaggedTexts = st.tag_sents(allTexts)
    #now put the tagged texts back in the dictionary in the same order
    for idx in range (0, len(allReviews)):
        allReviews[idx]['POStaggedText'] = allTaggedTexts[idx]
    return reviewsDict


def remove_chars():
    path = tagedDataPath 
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file_name in onlyfiles:
        fo = FileOperations(path + file_name)
        jsons = fo.get_json()
        #print jsons
        fo.write_to_file(jsons, path + file_name + ".pure")

shutil.rmtree(tagedDataPath)
os.makedirs(tagedDataPath)

taggedDict = getReviewDictWithTagging()
UtilityFunctions.pickleListOfObjects(pickleFolder, pickleFile, [taggedDict])


#remove_chars()
