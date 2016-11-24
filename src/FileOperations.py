
import xml.etree.ElementTree
import pickle
import xmldict




#===============================================================================
# 
#===============================================================================
def loadAndGetRawDataFromPickle(pickleFolder, pickleFile):
    '''
    @summary: Read the function name
    '''
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
    return (restaurantTrainDict,restaurantTestDict,laptopTrainDict, laptopTestDict)
#===============================================================================
# 
#===============================================================================


class FileOperations:
    def __init__(self, file_name):
        self.file_name = file_name
        f = open(file_name, 'r')
        self.text = f.read()
        f.close()

    #read the json file
#     def get_json(self):
#         print ("Loading json...")
#         self.jsons = []
#         lines = self.text.split('\n');
#         for line in lines:
#             try:
#                 curr = json.loads(line)
#                 for i in range(len(curr)):
#                     curr[i][0] = re.sub('[^a-zA-Z]+', '', curr[i][0])
#                 self.jsons.append(curr)
#             except:
#                 pass
#         self.num_lines = len(self.jsons)
#         return self.jsons

    def get_xml(self):
        self.xml_root = xml.etree.ElementTree.parse(self.file_name).getroot()
        return self.xml_root

    
    '''
        Edit this function to extract the aspects and polarity, and all the information
    '''
    def get_sentences(self):
        sentences = []
        for sentence in self.xml_root:
            for text in sentence.findall('text'):
                sentences.append(text.text)
        return sentences
#------------------------------------------------------------------------------ 
    def convertXmlToDict(self):
        '''
        '''
        ret_xmlDict = {}
        with open(self.file_name, 'r') as content_file:
            content = content_file.read()
            ret_xmlDict = xmldict.xml_to_dict(content)
        return ret_xmlDict
            
#------------------------------------------------------------------------------ 


    



        

