import os
from nltk.parse.stanford import StanfordDependencyParser

os.environ['CLASSPATH']='/Users/zarzen/Development/stanford-parser-full-2015-12-09'

def main():
    dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    dep_graph = dep_parser.raw_parse('It\'s like 9 punds, but if you can look past it, it\'s GREAT!')
    for item in dep_graph:
        print(item)


if __name__ == "__main__":
    main()
