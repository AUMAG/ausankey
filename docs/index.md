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

## Other works (both Python and not)

* [SankeyMATIC web app](https://sankeymatic.com)
* [floweaver for Python](https://github.com/ricklupton/floweaver) by ricklupton
* [alluvial for R](https://github.com/mbojan/alluvial) by mbojan

# Interface

## Getting started

The data to plot is first created in a Pandas dataFrame:

```
import pandas as pd
data = pd.DataFrame([
    (“apple”,     1  , “apple”,     0.5),
    (“banana”,    2  , “banana”,    3  ),
    (“lime”,      0.5, “lime”,      0.2),
    (“blueberry”, 0.2, “blueberry”, 1  ),
    (“orange”,    1.5, “orange”,    1.5),
])
```
Note that there can be as many columns as you like and they are always presented in pairs of “label” then “weight”. (Unweighted diagrams – currently – would require you to simple put a weight of 1.0 for each label.)

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


## Colours

You can customise the colours either by changing the Matplotlib colormap:
```
sky.sankey(data,colormap=“jet”)
```
![Image with options](fruits_jet.png)

Or by manually choosing the colours:
```
color_dict = {
    ‘apple’:     ‘#f71b1b’,
    ‘blueberry’: ‘#1b7ef7’,
    ‘banana’:    ‘#f3f71b’,
    ‘lime’:      ‘#12e23f’,
    ‘orange’:    ‘#f78c1b’
}
sky.sankey(data,color_dict=color_dict)
```
![Image with options](fruits_colordict.png)

The opacity of the flows can be customised:
```
sky.sankey(data,alpha=0.3)
```
![Image with options](fruits_alpha.png)


## Order of entries (sorting)

The order of the entries is top to bottom corresponding to first to last in the data frame.

The entries can be sorted highest to lowest:
```
sky.sankey(data,sorting=1)
```
![Image with options](fruits_sort_p1.png)

Or lowest to highest:
```
sky.sankey(data,sorting=-1)
```
![Image with options](fruits_sort_n1.png)


## Labels

If the data is generated externally it may not be convenient to edit the label text in the source. The typeset labels can be specified using a dictionary of lookup strings:
```
label_dict = {
    'apple':     'Apple',
    'blueberry': "B'berry",
    'banana':    'Banana',
    'lime':      'Lime',
    'orange':    'Orange'
}
sky.sankey(data,label_dict=label_dict)
```
![Image with options](fruits_labeldict.png)

Note that the dictionary does not need to contain an entry for each label. 


## Titles

Titles for each column of data can be added:
```
sky.sankey(data,titles=["Summer","Winter"])
```
![Image with options](fruits_titles.png)

Titles can be placed `"top"`, `"bottom"`, or `"both"`:
```
sky.sankey(data,
    titles = ["Summer","Winter"],
    title_side = "bottom",
)
```
![Image with options](fruits_titles_bottom.png)

Titles can also be placed “outside” the plot area, with default spacing intending to be placed outside the frame:
```
sky.sankey(data,
    titles = ["Summer","Winter"],
    frame_side = "both",
    title_loc = "outer",
)
```
![Image with options](fruits_titles_outer.png)

## Vertical Alignment

The vertical alignment of the diagram can be  `"top"`, `"bottom"`, or `"center"`:
```
sky.sankey(data,valign = "center")
```
![Image with options](fruits_valign.png)


## Frames

Horizontal framing can be placed `"top"`, `"bottom"`, or `"both"`: 
```
sky.sankey(data,frame_side = "both")
```
![Image with options](fruits_frame.png)

The frame can be coloured:
```
sky.sankey(data,
    frame_side=“both”,
    frame_color=“#62dcbe”,
 )
```
![Image with options](fruits_frame_color.png)

## Spacing

A number of parameters can be set to customise the spacing and layout of the diagram. These parameters are normalised against the diagram height or width according to which direction they are oriented. 
```
sky.sankey( data,
            titles = [“Summer”,”Winter”],
            title_side  = “both”,
            frame_side  = “both”,
            sorting     = -1,
            valign      = “center”,
            # spacing parameters:
            bar_gap     = 0.01 ,
            bar_width   = 0.1 ,
            frame_gap   = 0.2 ,
            label_width = 0.3 ,
            label_gap   = 0.02,
            title_gap   = 0.1 ,
          )
 ```
![Image with options](fruits_spacing.png)
