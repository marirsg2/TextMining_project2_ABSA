from FileOperations import FileOperations
import os
from nltk.tag.stanford import StanfordPOSTagger
import json
from os import listdir
from os.path import isfile, join

def tag_text():
    file_name = "./data/Restaurants_Train.xml"

    os.environ['CLASSPATH']='/home/sol315/Downloads/stanford-postagger-2015-12-09/stanford-postagger.jar'
    os.environ['STANFORD_MODELS']='./models/english-left3words-distsim.tagger'

    fo = FileOperations(file_name)
    fo.get_xml()
    sentences = fo.get_sentences()

    st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
    f = open('taged-' + file_name[7:-4] + '.json', 'a')
    cur = 0

    for line in sentences:
        cur += 1
        print (cur, cur * 100 / len(sentences), '%')
        res = st.tag(line.split())
        json_tag = json.dumps(res)
        f.write(json_tag)
        f.write('\n')
    f.close()

def remove_chars():
    path = '../taged-data/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file_name in onlyfiles:
        fo = FileOperations(path + file_name)
        jsons = fo.get_json()
        #print jsons
        fo.write_to_file(jsons, path + file_name + ".pure")

#tag_text()
remove_chars()
