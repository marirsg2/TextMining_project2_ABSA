


================================WORK for Zhen========================================

TFIDF instead of frequency method

===========================================================================================

================================WORK for Song===============================================

1) Probability of a noun being an aspect

===========================================================================================

================================WORK For Ram==============================================

0) loading raw data into another file.

TO DO
1) NLTK collocations from all the reviews in both categories.Then filter by occurrence (remove if less than 3 times)
http://www.nltk.org/howto/collocations.html

2)  use Doc 2 Vec for category identification. Train on labelled reviews with the category being laptop or restaurant.
		The idea is common nouns will not be strongly linked to either category (they are quite different),
		BUT the nouns that are strongly related/unique to one category will have a high similarity.
		typically you need the synset of the word to be accurate. Collocations will help better.

-------DONE WORK

1) Use NLTK wordnet lexicon and see if you can identify aspects better ? review the plan in the text file
			This FAILED, due to inadequate domain knowledge to detect overlaps



===========================================================================================


