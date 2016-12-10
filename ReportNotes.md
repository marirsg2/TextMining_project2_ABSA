## Task3 ##

data set contains such categories will cause problem

```
    <sentence id="3367">
        <text>Best of all is the warm vibe, the owner is super friendly and service is fast.</text>
        <aspectTerms>
            <aspectTerm term="vibe" polarity="positive" from="24" to="28"/>
            <aspectTerm term="owner" polarity="positive" from="34" to="39"/>
            <aspectTerm term="service" polarity="positive" from="62" to="69"/>
        </aspectTerms>
        <aspectCategories>
            <aspectCategory category="service" polarity="positive"/>
            <aspectCategory category="ambience" polarity="positive"/>
        </aspectCategories>
    </sentence>
```

cannot distinguish the connection between aspects and aspectCategory.

I have counted some numbers to analysis overall documents.
```
one category: 2468
one category and one aspect: 886
one category and multi aspects: 593
one category and No aspect: 989
multi categories: 576
multi categories and one aspect: 138
multi categories and multi aspects: 406
multi categories and No aspect: 32
```

