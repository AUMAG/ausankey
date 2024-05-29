# The `ausankey` package for Python


## Introduction

This Python package is used for creating diagrams like this, often known as Sankey diagrams:

![Image with options](frame3_pretty.png)

Currently, the package only supports flows in the horizontal direction (left-right).


## History

This package is a fork and extension of pysankey, which is represented by the following main contenders:

* Original [pysankey](https://github.com/anazalea/pySankey) by anazalea (no longer maintained)
* Forked [pysankey](https://github.com/Pierre-Sassoulas/pySankey/) by Pierre-Sassoulas
* [pysankey2](https://github.com/SZJShuffle/pySankey2/) by SZJShuffle

I started redeveloping the package independently to learn more about Python programming, and by the time I was done it was too late to try and resync with one of these forks. Hence, another fork!


## Documentation

* Getting started — see below
* [User interface](interface/)
* [Examples](examples/)
* [Changelog](CHANGELOG/)
* [Code reference documentation](reference/)


## Other works (both Python and not)

* [SankeyMATIC web app](https://sankeymatic.com)
* [floweaver for Python](https://github.com/ricklupton/floweaver) by ricklupton
* [alluvial for R](https://github.com/mbojan/alluvial) by mbojan
 

## Getting started

The data to plot is first created in a Pandas dataFrame:

```
import pandas as pd
data = pd.DataFrame(
    [
        ("apple", 100, "apple", 50),
        ("banana", 200, "banana", 30),
        ("lime", 50, "lime", 20),
        ("blueberry", 20, "blueberry", 10),
        ("orange", 150, "orange", 150),
    ]
)
```
Note that there can be as many columns as you like and they are always presented in pairs of “label” then “weight”. (Unweighted diagrams – currently – would require you to simple put a weight of 1.0 for each label.)

A three column dataset might look like:
```
data3 = pd.DataFrame(
    [
        ("a", 3, "ab", 6, "a" , 3),
        ("a", 3, "ba", 2, "ba", 1),
        ("c", 5, "cd", 3, "d" , 6),
        ("b", 2, "ba", 2, "ba", 1),
        ("b", 2, "ab", 2, "a" , 3),
        ("d", 6, "cd", 1, "d" , 3),
        ("e", 2, "e" , 3, "e" , 8),
    ]
)
```
Rather than manually typing out the dataFrame, you can also import it from a CSV file or similar:
```
import pandas as pd
data = pd.read_csv(‘pysankey/tests/fruit.csv’)
```
(You may need to be careful about whether the first row is considered to be data or column headers.)

Once you have the data, the diagram is plotted simply using the `sankey` function:
```
import ausankey as sky
sky.sankey(data)
```
which produces:
![Image with options](fruits_default.png)

There are a ton of customisation options set using a keyval interface. See the [user interface documentation](interface/) for details. 