"""
Author: Zhen Zhang(Zen)
Email: zhza16@lehigh.edu

"""
"""
function get_aspects will get the possible aspects based on frequency information
"""

from config_parser import pickleFile, pickleFolder
import FileOperations


def load_train_sentences():
    (restaurantTrainDict,restaurantTestDict,laptopTrainDict, laptopTestDict)\
        = FileOperations.loadAndGetRawDataFromPickle(pickleFolder, pickleFile)
    rst_train_sentences = restaurantTrainDict['sentences']['sentence']
    lptp_train_sentences = laptopTrainDict['sentences']['sentence']
    return rst_train_sentences, lptp_train_sentences


def put_word2dict(aspects, word):
    word = word.lower()
    if word in aspects:
        aspects[word] += 1
    else:
        aspects[word] = 1


def get_poss_aspects(all_reviews):
    """
    retain all possible NN and NNS
    """
    aspects_v = {}
    for review in all_reviews:
        for sent in review['POStaggedText']:
            for item in sent:
                word = item[0]
                tag = item[1]
                if tag == 'NN' or tag == 'NNS':
                    put_word2dict(aspects_v, word)

    return aspects_v


def remove_low_freq(aspects, rate, data_size):
    """
    remove low frequent nouns
    """
    del_list = []
    for word in aspects:
        freq = aspects[word]
        if freq < rate*data_size:
            del_list.append(word)
    for word in del_list:
        del aspects[word]


def get_aspects(low_freq=True, mutual_asp_rm=False,
                low_freq_rate = 0.01, remove_top=1):
    """
    get aspects vocabulary restaurant and laptop

    Args:
    low_freq(boolean): if set true, it will remove the low frequent words
    low_freq_rate(float): default remove frequency lower than 1% of total number reviews
    mutual_asp_rm(boolean): remove nouns in both laptop reviews and restaurant reviews
    remove_top(int): remove the most frequent words

    Returns:
    rst_aspects_v(dict): the vocabulary contains possible aspects from frequency based method
                         keys are words, value are frequency of that word
    lptp_aspects_v(dict): possible aspects of laptop

    """
    restaurant_sentences, laptop_sentences = load_train_sentences()
    lptp_aspects_v = get_poss_aspects(laptop_sentences)
    rst_apsects_v = get_poss_aspects(restaurant_sentences)
    # remove low frequent words
    if low_freq:
        remove_low_freq(lptp_aspects_v, low_freq_rate, len(laptop_sentences))
        remove_low_freq(rst_apsects_v, low_freq_rate, len(restaurant_sentences))

    # remove mutual aspects
    if mutual_asp_rm:
        remove_mutual_aspects(rst_apsects_v, lptp_aspects_v)

    remove_top_freq(lptp_aspects_v, remove_top)
    remove_top_freq(rst_apsects_v, remove_top)

    return rst_apsects_v, lptp_aspects_v


def remove_mutual_aspects(asp1, asp2):
    del_l= []

    for word in asp1:
        if word in asp2:
            del_l.append(word)
    for word in del_l:
        del asp1[word]
        del asp2[word]


def remove_top_freq(aspects, remove_n):
    """
    remove top frequent word,
    hope to remove some words like it it's
    """
    sorted_keys = sorted(aspects, key=aspects.__getitem__, reverse=True)
    del_words = sorted_keys[0:remove_n]
    for w in del_words:
        del aspects[w]


def main():
    """main for text"""
    rst_asp_v, lptp_asp_v = get_aspects(low_freq_rate = 0.005, remove_top=2)
    print(rst_asp_v)
    print('='*10)
    print(lptp_asp_v)


if __name__ == "__main__":
    main()
