from FileOperations import FileOperations
import os
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser
from os import listdir
from os.path import isfile, join
import UtilityFunctions
import depParsing 

tagedDataPath = '../taged-data/'
pickleFolder = '../PickledData/'
pickleFile = 'preProcessedData.p'

def getReviewDictsWithTagging():
    #setup all the variables needed to extract and tag the reviews
    file_names = ["../data/Restaurants_Train.xml","../data/restaurants-trial.xml","../data/Laptops_Train.xml",
                  "../data/laptops-trial.xml"]
    os.environ['CLASSPATH'] = os.pathsep + '../stanford-parser-full-2015-12-09' + \
                                                    os.pathsep + '../stanford_postagger/stanford-postagger.jar'
    os.environ['STANFORD_MODELS']='../stanford_postagger/models/english-left3words-distsim.tagger'
    os.environ['JAVAHOME']= "C:\\Program Files\\Java\jre1.8.0_71\\bin"    
    dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
    
    listOfDicts = []
    for file_name in file_names:
        fo = FileOperations(file_name)
    
    #this is a much easier way to convert an xml file directly to a dictionary in python to access data.
        reviewsDict = fo.convertXmlToDict()
        allReviews = reviewsDict['sentences']['sentence']
        allReviewTexts = [x['text'] for x in allReviews]
        # Nowl store each review as a list of sentences 
        allReviewsAsSentencesList = [] #eg: [ "The laptop was good", "The price was expensive" ]
        for singleReview in allReviewTexts:
            #add the list of sentences
            allReviewsAsSentencesList.append(depParsing.seg_text(singleReview))
        
        
        #need a list map that has the end index in it. So if a review has 3 sentences, and the first index is 4,
        # then the value at index 4 is 7
        
        allReviewsAsPOStaggedList = []
        allReviewsAsDEPStaggedList = []
        for singleReview in allReviewsAsSentencesList:
            #here each singleReview is a list of sentences eg: [ "The laptop was good", "The price was expensive" ]
            tokenizedSentences = [x.split() for x in singleReview]
            allReviewsAsPOStaggedList.append(st.tag_sents(tokenizedSentences))
            try:
                generator_dependencyGraphs = dep_parser.raw_parse_sents(singleReview)
            except:
                print("error with ", singleReview)
                generator_dependencyGraphs  = []
            for singleGraph in generator_dependencyGraphs:
                g = list(singleGraph) #convert into a list from a generator (iterator)
                if len(g) > 0:
                    listNodeDicts = []
                    for node in g[0].nodes:
                        nodeDict = g[0].nodes[node]
                        listNodeDicts.append(nodeDict)                                        
                    allReviewsAsDEPStaggedList.append(listNodeDicts)
                else:
                    allReviewsAsDEPStaggedList.append([])
                     
                            
        #Put the tagged texts back in the dictionary in the same order. The indexes line up, so this makes it easy
        for idx in range (0, len(allReviews)):
            allReviews[idx]['POStaggedText'] = allReviewsAsPOStaggedList[idx]
            allReviews[idx]['DEPStagging'] = allReviewsAsDEPStaggedList[idx]
        listOfDicts.append(reviewsDict)
    return listOfDicts
#===============================================================================
# 
#===============================================================================

def remove_chars():
    path = tagedDataPath 
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file_name in onlyfiles:
        fo = FileOperations(path + file_name)
        jsons = fo.get_json()
        #print jsons
        fo.write_to_file(jsons, path + file_name + ".pure")
#=======================================================================
# 
#=======================================================================

if __name__ == "__main__":
    [restaurantTrain,restaurantTrial,laptopTrain,laptopTrial] = getReviewDictsWithTagging()
    UtilityFunctions.pickleListOfObjects(pickleFolder, pickleFile, 
                                         [restaurantTrain,restaurantTrial,laptopTrain,laptopTrial])

    #remove_chars()
