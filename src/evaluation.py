import depParsing
import frequencyBased
import TF_IDF
import file_operations



def evaluate():

    freq_rst_asp, freq_lptp_asp = frequencyBased.get_aspects()
    tfidf_rst_asp, tfidf_lptp_asp = TF_IDF.get_aspects()
    rst_com, lptp_com = depParsing.get_aspects()

    # new syntax available py3.5 to combine dictionary
    freq_combined_rst_aspects = {**freq_rst_asp, **rst_com}
    freq_combined_lptp_aspects = {**freq_lptp_asp, **lptp_com}

    tfidf_combined_rst_aspects = {**tfidf_rst_asp, **rst_com}
    tfidf_combined_lptp_aspects = {**tfidf_lptp_asp, **lptp_com}

    # Train set
    train_rst_sentences, train_lptp_sentences = frequencyBased.load_train_sentences()
    print('$' * 10 + "On training data: " + '$'*10)
    print('*'*10 +"Frequency based method : "+ '*'*10)
    print('-'*10 + "Restaurant" + '-'*10)
    eval_on_one_set(train_rst_sentences, freq_combined_rst_aspects)
    print('-' * 10 + "Laptop" + '-' * 10)
    eval_on_one_set(train_lptp_sentences, freq_combined_lptp_aspects)
    print('*'*10 + "End frequency" + '*'*10)

    print("TF-IDF: " + '*'*10 )
    eval_on_one_set(train_rst_sentences, tfidf_combined_rst_aspects)
    eval_on_one_set(train_lptp_sentences, tfidf_combined_lptp_aspects)
    print('*' * 10 + "End TF-IDF" + '*' * 10)

    print('='*80)
    # TEST set
    print('On Test data')
    test_rst, test_lptp = frequencyBased.load_test_sentences()
    print('*'*10 + "Frequency based method : " + '*'*10)

    print('-' * 10 + "Restaurant" + '-' * 10)
    eval_on_one_set(test_rst, freq_combined_rst_aspects)
    print('-' * 10 + "Laptop" + '-' * 10)
    eval_on_one_set(test_lptp, freq_combined_lptp_aspects)

    print('*' * 10 + "End frequency" + '*' * 10)

    print('*'*10 + "TF-IDF: " + '*'*10)
    print('-' * 10 + "Restaurant" + '-' * 10)
    eval_on_one_set(test_rst, tfidf_combined_rst_aspects)
    print('-' * 10 + "Laptop" + '-' * 10)
    eval_on_one_set(test_lptp, tfidf_combined_lptp_aspects)
    print('*' * 10 + "End TF-IDF" + '*' * 10)



def eval_on_one_set(labeled_data, aspects_dict):
    """
    :param labels:
    :param aspects_dict:
    :return:
    """
    TP = 0
    FN = 0
    FP = 0
    for sent in labeled_data:
        _TP = 0
        _FN = 0
        _FP = 0
        text = sent['text']

        true_aspects = get_aspects(sent)
        poss_aspects = []

        for aspect in aspects_dict:
            if aspect in text:
                poss_aspects.append(aspect)
        del_overlap = []
        for word in poss_aspects:
            for another in poss_aspects:
                if another != word and word in another:
                    del_overlap.append(word)
        del_overlap = set(del_overlap)
        for word in del_overlap:
            poss_aspects.remove(word)

        _TP = len(set(true_aspects).intersection(poss_aspects))

        _FN = len(true_aspects) - _TP
        _FP = len(poss_aspects) - _TP
        TP += _TP
        FN += _FN
        FP += _FP
        # print('true aspects: ' + str(true_aspects))
        # print('possible aspects: ' + str(poss_aspects))
        # print(text)
        # print('TP: ' + str(_TP))
        # print('FN: ' + str(_FN))
        # print('FP: ' + str(_FP))
        # print('*' * 20)

    precision = float(TP) / (TP+FP)
    recall = float(TP) / (TP + FN)
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print('TP: ' + str(TP))
    print('FN: ' + str(FN))
    print('FP: ' + str(FP))
    return precision, recall


def get_aspects(sent):
    ret = []
    if 'aspectTerms' in sent:
        aspects = sent['aspectTerms']
        aspects = aspects['aspectTerm']
        if type(aspects) == list:
            for asp in aspects:
                ret.append(asp['@term'])
        else:
            aspect_word = aspects['@term']
            ret.append(aspect_word)
    else:
        # print(sent)
        pass
    return ret

if __name__ == "__main__":
    evaluate()