This file documents the necessary steps needed for integrating methods
substituting topic modelling

Essentially, one needs to write a function that takes in the following
**input parameters** and return the following **output parameters**

# Input parameters:

## input_file
`input_file`: path to standard input file, this file is of the format as
any of the `jsonlist` file in folder `data`

So, it is the case that you have to begin from tokenization (sorry I got
that wrong yesterday). My tokenizer for Chinese is implemented in
`preprocessing.py`.

## data_output_dir
`data_output_dir`: path to a folder where you can store intermediate data
(use it at your discreteion, you can choose to not use it at all)

# Output parameters:

## articles
`articles`: for each article given in `input_file` (namely each line),
you need to return the following list:

```python
[
  Article(fulldate=1951, ideas=set([32, 48, 3, 4, 5, 7, 10, 15, 16, 20, 24, 25, 29])), 
  Article(fulldate=1951, ideas=set([32, 2, 35, 41, 14, 17, 19, 20, 23, 25, 26, 28])), 
  Article(fulldate=1951, ideas=set([33, 7, 41, 13, 45, 16, 18, 23, 27])), 
  Article(fulldate=1951, ideas=set([0, 1, 2, 32, 8, 9, 45, 23, 28, 31])), 
  Article(fulldate=1951, ideas=set([34, 37, 7, 9, 43, 13, 23, 25, 26, 27])), 
  Article(fulldate=1951, ideas=set([32, 1, 36, 7, 12, 13, 14, 49, 22, 23, 27])), 
  Article(fulldate=1951, ideas=set([1, 36, 5, 33, 40, 42, 11, 44, 17, 19, 23, 24, 25, 26, 37, 31])), 
  Article(fulldate=1951, ideas=set([32, 1, 4, 37, 7, 40, 10, 16, 49, 48, 23, 25, 29])), 
  Article(fulldate=1951, ideas=set([7, 9, 13, 49, 20, 23, 27])), 
  Article(fulldate=1951, ideas=set([32, 34, 7, 41, 10, 12, 13, 14, 15, 19, 23, 26, 27]))
]
```

This `Article` constructor can be found in `utils.py`, where it is given as:
`IdeaArticle = collections.namedtuple("Article", ["fulldate", "ideas"])`
following that you can just call
``articles.append(utils.IdeaArticle(fulldate=int(data["date"]), ideas=ideas))``
as done at Line 68 of `mallet_topics.py`

It's fine for your script to output a file with a format similar to this
(you don't actually have to construct these Python objects). As long as
I can easily get that into this desired format it's fine.

## vocab

This seems to be optional. Neglect for now: Returns a dictionary

```
{0: u'--', 1: u'u.s.', 2: u'market', 3: u'would', 4: u'stock', 5: u'economic', 6: u'new', 7: u'last', 8: u'economy', 9: u'one', 10: u'prices', 11: u'also', 12: u'first', 13: u'since', 14: u'year', 15: u'could', 16: u'percent', 17: u'many', 18: u'investors', 19: u'government', 20: u'may'}
```

## idea_names

Returns a dictionary matching idea index in `articles` with the vocab words:

```python
{0: u'federal reserve,fed,banks,money,credit,rate,board,bank,interest,yesterday', 
 1: u'bond,treasury,bonds,yield,investors,prices,interest rates,yields,government,securities', 
 2: u'would,house,bill,congress,senate,committee,legislation,members,vote,federal', 
 3: u'rose,report,month,index,fell,reported,since,showed,last,economic', 
 4: u"fed,u.s.,federal reserve,economy,economic,low,policy,fed's,inflation,central bank", 
 5: u'production,industry,auto,steel,union,new,companies,industries,industrial,car', 
 6: u'index,stocks,dow jones,stock,industrial average,investors,market,fell,rose,points', 
 7: u'market,stock,new york,,average,today,points,volume,trading,stocks,dow jones', 
 8: u'federal,government,law,u.s.,legal,rules,office,court,securities,regulators', 
 9: u'prices,price,inflation,oil,energy,food,higher,consumer,oil prices,increase', 
 10: u'investors,funds,stock,market,investment,money,fund,stocks,financial,cash', 
 11: u'tax,would,taxes,income,cut,increase,new,rates,proposal,also', 
 12: u"dollar,u.s.,currency,yen,trading,euro,new york,japanese,dollar's,late", 
 13: u'last,week,time,first,two,since,week,,three,days,four', 
 14: u'earnings,sales,company,profit,million,revenue,cents,results,reported,year'}
```