# The ausankey package

## Introduction

This Python package is used for creating diagrams like this, often known as Sankey diagrams:

![Image with options](frame3_many.png)

Currently, the package only supports flows in the horizontal direction (left-right).

## History

This package is a fork and extension of pysankey, which is represented by the following main contenders:

* Original [pysankey](https://github.com/anazalea/pySankey) by anazalea 
* Forked [pysankey](https://github.com/Pierre-Sassoulas/pySankey/) by Pierre-Sassoulas
* [pysankey2](https://github.com/SZJShuffle/pySankey2/) by SZJShuffle

I started redeveloping the package independently to learn more about Python programming, and by the time I was done it was too late to try and resync with one of these forks. Hence, another fork!

## Other works

* [alluvial for R](https://github.com/mbojan/alluvial) by mbojan

# Interface

## Getting started

The data to plot is first created in a Pandas dataFrame:

```
import pandas as pd
data = pd.DataFrame([
  (“a”,1.0,”ab”,2.0),
  (“a”,1.0,”ba”,0.8),
  (“c”,1.5,”cd”,0.5),
  (“b”,0.5,”ba”,0.8),
  (“b”,0.5,”ab”,0.8),
  (“d”,2.0,”cd”,0.4),
  (“e”,1.0,”e”,1.0),
])
```
Note that there can be as many columns as you like and they are always presented in pairs of “label” then “weight”. (Unweighted diagrams – currently – would require you to simple put a weight of 1.0 for each label.)

Rather than manually typing out the dataFrame, you can also import it from a CSV file or similar:
```
import pandas as pd
data = pd.read_csv(
    ‘pysankey/tests/fruit.csv’,
    sep=‘,’,
)
```
(You may need to be careful about whether the first row is considered to be data or column headers.)

Once you have the data, the diagram is plotted simply using the `sankey` function:
```
import pysankey as sky
sky.sankey(data)
```
which produces:
![Image with options](fruits_default.png)
