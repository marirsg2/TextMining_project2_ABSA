import os
from nltk.parse.stanford import StanfordDependencyParser
import nltk.data


os.environ['CLASSPATH']='/Users/zarzen/Development/stanford-parser-full-2015-12-09'


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
            node = g[0].nodes[node]
            for dep in node['deps']:
                if dep == 'compound':
                    print('-'*15)
                    print(node)


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
