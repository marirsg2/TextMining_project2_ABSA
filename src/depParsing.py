import os
from nltk.parse.stanford import StanfordDependencyParser
import nltk.data


os.environ['CLASSPATH'] = os.pathsep + '../stanford-parser-full-2015-12-09' + \
                                                    os.pathsep + '../stanford_postagger/stanford-postagger.jar'
os.environ['STANFORD_MODELS'] ='../stanford_postagger/models/english-left3words-distsim.tagger'
os.environ['JAVAHOME'] = "C:\\Program Files\\Java\jre1.8.0_71\\bin"    


def seg_text(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    ss = sent_detector.tokenize(text.strip())
    return ss

def get_compound(text, _parser):
    sents = seg_text(text)
    depg = _parser.raw_parse_sents(sents)
    for g in depg:
        g = list(g)
        for node in g[0].nodes:
            nodeDict = g[0].nodes[node]
            for dep in nodeDict['deps']:
                if dep == 'compound':
                    print('-'*15)
                    print(nodeDict)


def main():
    dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    dep_graph = dep_parser.raw_parse('It\'s like 9 punds, but if you can look past it, it\'s GREAT!')
    for item in dep_graph:
        print(item)

    tt = '''
    I previously purchased a 13" macbook (had pro specs and was aluminum style) which had a
    nvidia 9800 (If I am not mistaken) and it had major heating issues. The battery doesn't
    last long but I'm sure an upgrade battery would solve that problem.
    I charge it at night and skip taking the cord with me because of the good battery life.
    '''
    get_compound(tt, dep_parser)

if __name__ == "__main__":
    main()
