import depParsing
import frequencyBased


def evaluate():
    """

    :return:
    """
    rst_asp_v, lptp_asp_v = frequencyBased.get_aspects(low_freq_rate=0.005, remove_top=2, mutual_asp_rm=True)
    rst_com_v, lptp_com_v = depParsing.get_aspects()

    # new syntax available py3.5 to combine dictionary
    combined_rst_aspects = {**rst_asp_v, **rst_com_v}
    combined_lptp_aspects = {**lptp_asp_v, **lptp_com_v}

    # eval on train
    restaurant_sentences, laptop_sentences = frequencyBased.load_train_sentences()
    eval_on_one_set(restaurant_sentences, combined_rst_aspects)
    eval_on_one_set(laptop_sentences, combined_lptp_aspects)


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
        print('true aspects: ' + str(true_aspects))

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

        print('possible aspects: ' + str(poss_aspects))
        print(text)

        _TP = len(set(true_aspects).intersection(poss_aspects))

        _FN = len(true_aspects) - _TP
        _FP = len(poss_aspects) - _TP
        TP += _TP
        FN += _FN
        FP += _FP
        print('TP: ' + str(_TP))
        print('FN: ' + str(_FN))
        print('FP: ' + str(_FP))
        print('*' * 20)

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