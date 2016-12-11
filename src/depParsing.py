"""
Author: Zhen Zhang(Zen)
Email: zhza16@lehigh.edu

invoke get_aspects() function for obtaining possible aspects from compound relationship

"""

import os
import nltk
from nltk.parse.stanford import StanfordDependencyParser
import file_operations
import frequencyBased
from config_parser import pickleFile, pickleFolder


def load_train_sentences():
    (restaurantTrainDict, restaurantTestDict, laptopTrainDict, laptopTestDict) \
        = file_operations.loadAndGetRawDataFromPickle(pickleFolder, pickleFile)
    rst_train_sentences = restaurantTrainDict['sentences']['sentence']
    lptp_train_sentences = laptopTrainDict['sentences']['sentence']
    return rst_train_sentences, lptp_train_sentences


def seg_text(text):
    """
    helper function
    segment the text into sentences

    Returns:
        (list)a list of sentences
    """
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    ss = sent_detector.tokenize(text.strip())
    return ss


def get_depG():
    """
    this function used for testing purpose

    Returns:
        (dependency graph) for testing
    """
    os.environ['CLASSPATH'] = '/Users/zarzen/Development/stanford-parser-full-2015-12-09'
    dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

    tt = '''
    The programs that come standard with the Leopard running system are enough for the average person to run all the basics.
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
            if node['tag'] == 'NN' or node['tag'] == 'NNS' \
                    or compound_node['tag'] == 'NN' or compound_node['tag'] == 'NNS':
                aspects_list.append([current_word, compound_word])

    return aspects_list


def get_compound2(depG):
    """
    Args:
    depG (list): the input is one dependency Graph

    Returns:
    aspects(list): contains pairs of compound NN, possible aspects

    """

    aspects_list = []
    for node in depG:
        if 'compound' in node['deps']:
            current_word = node['word']
            words_list = []
            for pos in node['deps']['compound']:
                compound_node = get_node_with_address(pos, depG)
                compound_word = compound_node['word']
                words_list.append(compound_word)

            words_list.append(current_word)
            # if len(node['deps']['compound']) > 2:
            #     print(node)
            if node['tag'] == 'NN' or node['tag'] == 'NNS' or node['tag'] == 'NNP' \
                    or node['tag'] == 'NNPS':
                aspects_list.append(words_list)
            else:
                pass
                # print(compound_words)
                # print(node['tag'])

    return aspects_list


def get_poss_aspects(all_reviews):
    """
    get all possible compounds contains noun as aspects
    """
    aspects = {}
    for review in all_reviews:
        depGraphs = review['DEPStagging']
        for graph in depGraphs:
            aspects_list = get_compound(graph)
            for pair in aspects_list:
                put_aspect(aspects, pair)
    return aspects


def get_poss_aspects2(all_reviews):
    """
    get all possible compounds contains noun as aspects
    """
    aspects = {}
    for review in all_reviews:
        depGraphs = review['DEPStagging']
        for graph in depGraphs:
            aspects_list = get_compound2(graph)
            for pair in aspects_list:
                put_aspect(aspects, pair)
    return aspects


def put_aspect(aspects_dict, aspect):
    """
    Args:
        aspect(str)
    """
    aspect_str = ''
    for i in aspect:
        # i = i.lower()
        aspect_str += i
        aspect_str += ' '
    aspect_str = aspect_str.strip()
    if aspect_str in aspects_dict:
        aspects_dict[aspect_str] += 1
    else:
        aspects_dict[aspect_str] = 1


def get_aspects():
    """
    get possible aspects from train data through compound relationship

    Returns:
        vocabulary for laptop
        vocabulary for restaurant
    """
    rst_train, lptp_train = load_train_sentences()
    rst_aspects = get_poss_aspects(rst_train)
    lptp_aspects = get_poss_aspects(lptp_train)

    # remove low frequent
    # or if one of the word is in frequency words list
    rst_asp_freq, lptp_asp_freq = frequencyBased.get_aspects()

    rst_aspects = remove_low_freq(rst_aspects, rst_asp_freq)
    lptp_aspects = remove_low_freq(lptp_aspects, lptp_asp_freq)

    return rst_aspects, lptp_aspects


def remove_low_freq(poss_asp, verify_dict):
    """
    retain frequency greater than 1
    or one of the compound word is in verify_dict

    Returns:
        aspects are retained
    """
    retained_asp = {}
    for words in poss_asp:
        if poss_asp[words] > 1 or \
                word_in(verify_dict, words):
            retained_asp[words] = poss_asp[words]
    return retained_asp


def word_in(verify_dict, words):
    """
    Args:
    dict(dict): aspects extracted by frequency based method
    words(str): compound words extract from dependency parsing tree

    Returns:
        indicator(boolean)
    """
    words = words.split(' ')
    if words[0].strip() in verify_dict:
        return True
    elif words[1].strip() in verify_dict:
        return True
    else:
        return False


def get_node_with_address(address, depG):
    """
    quick fix for data problem.
    node are stored in list. but when adding node into list, we cannot guarantee
    the address is the same as index of node list
    """
    for node in depG:
        if node['address'] == address:
            return node


def test():

    print(get_compound2(get_depG()))
    # rst_asp, lptp_asp = get_aspects()
    # print('*' * 20)
    # print(rst_asp)
    # print('*' * 20)
    # print(lptp_asp)
    # print(len(lptp_asp))

    # rst_train, lptp_train = load_train_sentences()
    # rst_aspects1 = get_poss_aspects(rst_train)
    # lptp_aspects1 = get_poss_aspects(lptp_train)
    # rst_aspects2 = get_poss_aspects2(rst_train)
    # lptp_aspects2 = get_poss_aspects2(lptp_train)
    #
    # rst_count = 0
    # for key in rst_aspects1:
    #     if key not in rst_aspects2:
    #         rst_count += 1
    # lptp_count = 0
    # for key in lptp_aspects1:
    #     if key not in lptp_aspects2:
    #         lptp_count += 1
    # print(rst_count)
    # print(lptp_count)

if __name__ == "__main__":
    test()
