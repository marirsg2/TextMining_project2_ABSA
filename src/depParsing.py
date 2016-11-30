import os
from nltk.parse.stanford import StanfordDependencyParser
import nltk.data

os.environ['CLASSPATH']='/Users/zarzen/Development/stanford-parser-full-2015-12-09'


def seg_text(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    ss = sent_detector.tokenize(text.strip())
    return ss

def get_depG():
    dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    tt = '''
    I previously purchased a 13" macbook (had pro specs and was aluminum style) which had a
    nvidia 9800 (If I am not mistaken) and it had major heating issues. The battery doesn't
    last long but I'm sure an upgrade battery would solve that problem.
    I charge it at night and skip taking the cord with me because of the good battery life.
    '''
    tt = tt.strip()
    tt = tt.replace('\n', ' ')
    sents = seg_text(tt)
    depgs = dep_parser.raw_parse_sents(sents)
    depgs = list(depgs)
    depG = []
    g = depgs[-1]
    g = list(g)
    g = g[0]
    for node_idx in g.nodes:
        node_dict = g.nodes[node_idx]
        depG.append(node_dict)
    return depG


def get_compound(depG):
    """
    Args:
    depG (list): the input is one dependency Graph

    Returns:
    aspects(list): contains pairs of compound NN, possible aspects

    """

    aspects_list = []
    for node in depG:
        rel = node['rel']
        if rel == 'compound':
            current_word = node['word']
            head_address = node['head']
            compound_node = get_node_with_address(head_address, depG)
            compound_word = compound_node['word']
            if node['tag'] == 'NN' or node['tag'] == 'NNS'\
            or compound_node['tag'] == 'NN' or compound_node['tag'] == 'NNS':
                aspects_list.append([current_word, compound_word])

    return aspects_list

def get_node_with_address(address, depG):
    """
    quick fix for data problem.
    node are stored in list. but when adding node into list, we cannot guarantee
    the address is the same as index of node list
    """
    for node in depG:
        if node['address'] == address:
            return node


def get_compound_test(text, _parser):
    """

    """
    sents = seg_text(text)
    depg = _parser.raw_parse_sents(sents)
    for g in depg:
        g = list(g)
        for node in g[0].nodes:
            node = g[0].nodes[node]
            for dep in node['deps']:
                if dep == 'compound':
                    #print('-'*15)
                    #print(node)
                    word = node['word']
                    w_idx = node['deps']['compound'][0]
                    word2 = g[0].nodes[w_idx]['word']
                    print(word + ',' + word2)


def main():
    dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    dep_graph = dep_parser.raw_parse('It\'s like 9 punds, but if you can look past it, it\'s GREAT!')
    # for item in dep_graph:
    #     print(item)

    tt = '''
    I previously purchased a 13" macbook (had pro specs and was aluminum style) which had a
    nvidia 9800 (If I am not mistaken) and it had major heating issues. The battery doesn't
    last long but I'm sure an upgrade battery would solve that problem.
    I charge it at night and skip taking the cord with me because of the good battery life.
    '''
    #get_compound_test(tt, dep_parser)
    print(get_depG())

if __name__ == "__main__":
    main()
