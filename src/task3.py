"""
include evaluation
"""
import file_operations
from config_parser import pickleFile, pickleFolder


(restaurantTrainDict, restaurantTestDict, laptopTrainDict, laptopTestDict)\
    = file_operations.loadAndGetRawDataFromPickle(pickleFolder, pickleFile)
rst_train_sentences = restaurantTrainDict['sentences']['sentence']
rst_test_sentences = restaurantTestDict['sentences']['sentence']


def put_asp_cate(aspect, category, collector):
    """

    """
    if aspect in collector:
        cate_dict = collector[aspect]
        if category in cate_dict:
            cate_dict[category] += 1
        else:
            cate_dict[category] = 1
    else:
        collector[aspect] = {}
        collector[aspect][category] = 1


def get_asp2category():
    asp_category = {}
    for sent in rst_train_sentences:
        categories = sent['aspectCategories']['aspectCategory']
        if type(categories) is dict:
            if 'aspectTerms' in sent:

                aspects = sent['aspectTerms']['aspectTerm']
                if type(aspects) is dict:
                    #                 print(aspects)
                    put_asp_cate(aspects['@term'], categories['@category'], asp_category)
                else:
                    for asp in aspects:
                        put_asp_cate(asp['@term'], categories['@category'], asp_category)
        # contains multiple categories
        elif type(categories) is list:
            if 'aspectTerms' in sent:
                # print(sent['aspectTerms'])
                aspects = sent['aspectTerms']['aspectTerm']
                if type(aspects) is dict:
                    for cate in categories:
                        put_asp_cate(aspects['@term'], cate['@category'], asp_category)
                else:
                    for cate in categories:
                        for asp in aspects:
                            put_asp_cate(asp['@term'], cate['@category'], asp_category)
    asp2category = {}
    for asp in asp_category:
        categories = list(asp_category[asp].keys())
        most_freq_category = categories[0]
        for cate in categories:
            if asp_category[asp][cate] > asp_category[asp][most_freq_category]:
                most_freq_category = cate
        asp2category[asp] = most_freq_category

    return asp2category


def categories_count():
    one_category_c = 0
    one_cate_one_asp = 0
    one_cate_multi_asp = 0

    multi_cate = 0
    multi_cate_one_asp = 0
    multi_cate_multi_asp = 0
    for sent in rst_train_sentences:
        categories = sent['aspectCategories']['aspectCategory']
        if type(categories) is dict:
            one_category_c += 1
            if 'aspectTerms' in sent:
                # print(sent['aspectTerms'])
                aspects = sent['aspectTerms']['aspectTerm']
                if type(aspects) is dict:
                    one_cate_one_asp += 1
                else:
                    one_cate_multi_asp += 1
        elif type(categories) is list:
            # print(categories)
            multi_cate += 1
            if 'aspectTerms' in sent:
                # print(sent['aspectTerms'])
                aspects = sent['aspectTerms']['aspectTerm']
                if type(aspects) is dict:
                    multi_cate_one_asp += 1
                else:
                    multi_cate_multi_asp += 1

    print("one category: {0}".format(one_category_c))
    print('one category and one aspect: {0}'.format(one_cate_one_asp))
    print('one category and multi aspects: {0}'.format(one_cate_multi_asp))
    print('one category and No aspect: {0}'.format(one_category_c - one_cate_one_asp - one_cate_multi_asp))

    print('multi categories: {0}'.format(multi_cate))
    print('multi categories and one aspect: {0}'.format(multi_cate_one_asp))
    print('multi categories and multi aspects: {0}'.format(multi_cate_multi_asp))
    print('multi categories and No aspect: {0}'.format(multi_cate - multi_cate_one_asp - multi_cate_multi_asp))


def evaluation(verbose = True):
    """
    evaluation assume we can get the right aspects from sentences.

    :return:
    """

    asp2category = get_asp2category()

    print("*" * 20 + "Evaluation on Train data" + '*' * 20)
    # eval on train sentences
    eval_one(rst_train_sentences, asp2category, verbose)
    print("*" * 20 + "END Evaluation on Train data " + '*' * 20)

    print()
    print("*" * 20 + "Evaluation on Test data" + '*' * 20)
    # eval on test sentences
    eval_one(rst_test_sentences, asp2category, verbose)
    print("*" * 20 + "END Evaluation on Test data" + '*' * 20)


def eval_one(sentences, asp2category, verbose):
    """
    :param sentences: (list)
    :param asp2category: (dict) mapping from aspect to category
    :param verbose: (boolean) enable verbose mode or not
    :return:
    """
    TP = 0
    FN = 0
    FP = 0
    for sent in sentences:
        aspects = get_aspects(sent)
        true_categories = get_true_asp_category(sent)
        poss_categories = []
        for asp in aspects:
            if asp in asp2category:
                poss_categories.append(asp2category[asp])
        poss_categories = set(poss_categories)

        _TP = len(set(true_categories).intersection(poss_categories))
        _FN = len(true_categories) - _TP
        _FP = len(poss_categories) - _TP
        TP += _TP
        FN += _FN
        FP += _FP
        if verbose:
            print('true category: ' + str(true_categories))
            print('possible category: ' + str(poss_categories))
            print(sent['text'])
            print('TP: ' + str(_TP))
            print('FN: ' + str(_FN))
            print('FP: ' + str(_FP))
            print('*' * 20)

    precision = float(TP) / (TP + FP)
    recall = float(TP) / (TP + FN)
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print('TP: ' + str(TP))
    print('FN: ' + str(FN))
    print('FP: ' + str(FP))

    return precision, recall


def get_true_asp_category(sent):
    categories = sent['aspectCategories']['aspectCategory']
    if type(categories) is dict:
        return [categories['@category']]
    else:
        ret_categories = []
        for cate in categories:
            ret_categories.append(cate['@category'])
        return ret_categories


def get_aspects(sent):
    """
    get the aspect from sentence
    :param sent: sentence
    :return:
    """
    ret_asp = []
    if 'aspectTerms' not in sent:
        return ret_asp
    else:
        aspects = sent['aspectTerms']['aspectTerm']
        if type(aspects) is dict:
            ret_asp.append(aspects['@term'])
        else:
            for asp in aspects:
                ret_asp.append(asp['@term'])
        return ret_asp


def main():
    """
    :return:
    """
    print("=" *20 + "Data set structure analysis" + '='*20)
    categories_count()
    print()
    print("=" * 20 + "Evaluation " + '=' * 20)
    evaluation(verbose=True)

if __name__ == '__main__':
    main()
