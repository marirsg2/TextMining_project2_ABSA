from frequencyBased import load_train_sentences, get_poss_aspects, put_word2dict


def get_aspects():
    rst_train, lptp_train = load_train_sentences()
    rst_aspects = get_poss_aspects(rst_train)
    lptp_aspects = get_poss_aspects(lptp_train)

    outside_dict = get_outside_dict()

    rst_aspects = cal_TF_IDF(rst_aspects, outside_dict)
    lptp_aspects = cal_TF_IDF(lptp_aspects, outside_dict)

    rst_aspects = keep_top_freq(rst_aspects, 100)
    lptp_aspects = keep_top_freq(lptp_aspects, 100)

    return rst_aspects, lptp_aspects


def cal_TF_IDF(aspects, outside_dict):
    for word in aspects:
        _IDF = get_freq(word, outside_dict)
        aspects[word] = aspects[word] / float(_IDF)
    return aspects

def get_outside_dict():
    import nltk
    emma = nltk.corpus.gutenberg.words('austen-emma.txt')
    word_freq_dict = {}
    for word in emma[0:45000]:
        put_word2dict(word_freq_dict, word)
    return word_freq_dict


def get_freq(word, dict):
    if word in dict:
        return dict[word]
    else:
        return 1


def keep_top_freq(aspects, _n):
    """
    keep top tf-idf word,

    """
    sorted_keys = sorted(aspects, key=aspects.__getitem__, reverse=True)
    keep_words = sorted_keys[0:_n]
    ret = {}
    for word in keep_words:
        ret[word] = aspects[word]
    return ret


def test():
    print(get_aspects())


if __name__ == "__main__":
    test()