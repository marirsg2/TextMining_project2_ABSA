

@Ram:  I found this nice code xmldict that directly converts xml data to python dictionary. I tested it.
with this we can easily extract the data we need from each review. Each review is a sentence under the 
python dictionary. if you debug and print the dict, you can see what I mean. 

@Ram: My next step is to save the POS tagged version in the same dict for each sentence, and then pickle the dictionary
so we dont have to repeat this step every time.