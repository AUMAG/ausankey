# Interface

## Getting started

The data to plot is first created in a Pandas dataFrame:

```
import pandas as pd
data = pd.DataFrame(
    [
        (“apple”, 100, “apple”, 50),
        (“banana”, 200, “banana”, 30),
        (“lime”, 50, “lime”, 20),
        (“blueberry”, 20, “blueberry”, 10),
        (“orange”, 150, “orange”, 150),
    ]
)
```
Note that there can be as many columns as you like and they are always presented in pairs of “label” then “weight”. (Unweighted diagrams – currently – would require you to simple put a weight of 1.0 for each label.)

A three column dataset might look like:
```
data3 = pd.DataFrame(
    [
        (“a”, 3, “ab”, 6, “a” , 3),
        (“a”, 3, “ba”, 2, “ba”, 1),
        (“c”, 5, “cd”, 3, “d” , 6),
        (“b”, 2, “ba”, 2, “ba”, 1),
        (“b”, 2, “ab”, 2, “a” , 3),
        (“d”, 6, “cd”, 1, “d” , 3),
        (“e”, 2, “e” , 3, “e” , 8),
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
![Image with options](iface_fruits_default.png)


## Colours

You can customise the colours either by changing the Matplotlib colormap:
```
sky.sankey(data,colormap=“jet”)
```
![Image with options](iface_fruits_jet.png)

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
![Image with options](iface_fruits_colordict.png)

You can combine both approaches to use a colour map for most of the nodes and then override only some of them manually. (I.e., the `color_dict` does not need to have entries for all of the labels.)

The opacity of the flows and nodes can be customised with `flow_alpha` and `node_alpha` respectively:
```
sky.sankey(data,flow_alpha=0.3)
```
![Image with options](iface_fruits_alpha.png)


## Order of entries (sorting)

The order of the entries is top to bottom corresponding to first to last in the data frame.

The entries can be sorted highest to lowest:
```
sky.sankey(data,sort=“top”)
```
![Image with options](iface_fruits_sort_top.png)

Or lowest to highest:
```
sky.sankey(data,sort=“bottom”)
```
![Image with options](iface_fruits_sort_bot.png)

Or left in the order listed in the data:
```
sky.sankey(data,sort=“none”)
```
![Image with options](iface_fruits_sort_none.png)

The sort order of individual labels can be overidden using the `sort_dict`.
E.g., `sort_dict={“a”,0}` would sort label `a` to the bottom of each stage regardless of its weighted node values.

## Vertical Alignment

The vertical alignment of the diagram can be  `”top”`, `”bottom”`, or `”center”`:
```
sky.sankey(data,valign = “center”)
```
![Image with options](iface_fruits_valign.png)


## Labels

If the data is generated externally it may not be convenient to edit the label text in the source. The typeset labels can be specified using a dictionary of lookup strings:
```
label_dict = {
    ‘apple’:     ‘Apple’,
    ‘blueberry’: “B’berry”,
    ‘banana’:    ‘Banana’,
    ‘lime’:      ‘Lime’,
    ‘orange’:    ‘Orange’
}
sky.sankey(data,label_dict=label_dict)
```
![Image with options](iface_fruits_labeldict.png)

Note that the dictionary does not need to contain an entry for each label.

The locations of the labels can be specified according to whether they correspond to the nodes in the first, middle, or right of the diagram:

    label_loc = [ <loc_l> , <loc_m>, <loc_r> ]

Allowable values for `<loc_l>` and `<loc_r>` are `”left”`, `”right”`,  `”center”`,  `”top”`, or `”none”`.
`<loc_m>` also allows `”both”`. The default settings are:

    label_loc = [ “left”, “none”, “right” ]

When adjusting the position of the labels, some care
can be needed to avoid clashing with the printing
of the values. In these examples we just turn the values off.
```
sky.sankey(
    data3,
    label_loc=[“right”,”right”,”left”],
    value_loc=[“none”,”none”,”none”],
)
```
![Image with options](iface_frame3_labels.png)

Repeating the labels can be redundant in cases where labels
are repeated/duplicated in successive stages. Label
duplication can be turned off, which only prints a label
if it didn’t appear in the previous stage.
```
sky.sankey(
    data3,
    label_loc=[“right”,”right”,”left”],
    value_loc=[“none”,”none”,”none”],
    label_duplicate=False,
)
```
![Image with options](iface_frame3_labels_dup.png)

Sometimes you only need to label once. If the values fluctuate significantly one approach to successfully labelling can be to only label the largest valued node across all stages:

```
sky.sankey(
    data,
    label_largest = True,
)
```

The position of the label will still be inferred from the `label_loc` setting.

By default the node label only includes the textual string. 
To include the numerical value as well, set `label_values` to true:

```
sky.sankey(
    data,
    node_gap = 0.2,
    label_values = True,
    value_format = "0.1f"
)
```
![Image with options](iface_fruits_node_labels.png)

Although not shown here, for more complex plots some heuristics
are used to avoid printing redundant flow values (see next section).

When creating complex plots it is sometimes unavoidable that labels
overlap other elements of the graph. To increase the contrast in
these cases, a font outline can be added. The syntax is inherited
from the `matplotlib.patheffects` library:
```
sky.sankey(
    data,
    label_loc = [“right”, ”right”, ”left”],
    label_path_effects = {
        "linewidth": 2,
        "foreground": "black",
    },
    fontcolor = "white" ,
)
```
![Image with options](iface_fruits_labels_outline.png)


## Values

The numerical values for each (sub)flow are annotated by default. 
(It’s slightly confusing that labels refer to nodes whereas values
refer to flows.) These can be customised or turned off.

The locations of the values can be specified according to whether they correspond to the flows in the first, middle, or right of the diagram:

    value_loc = [ <loc_l> , <loc_m>, <loc_r> ]

Allowable values for `<loc_l>` and `<loc_r>` are `”left”`, `”right”`,  `”both”`, or `”none”`.
The default settings are:

    value_loc = [ “both”, “right”, “right” ]

These defaults are intended to a avoid clashes with the default `label_loc` settings.

When `"both"` is used, a flow which doesn't change size will display repeated values.
This behaviour can be controlled with `value_duplicate`:

```
sky.sankey(
    data,
    value_loc = ["both","both","both"],
    value_duplicate = False,
)
```
![Image with options](iface_fruits_value_dup.png)


## Titles

Titles for each column of data can be added:
```
sky.sankey(data,titles=[“Summer”,”Winter”])
```
![Image with options](iface_fruits_titles.png)

Titles can be placed `”top”`, `”bottom”`, or `”both”`:
```
sky.sankey(data,
    titles = [“Summer”,”Winter”],
    title_side = “bottom”,
)
```
![Image with options](iface_fruits_titles_bottom.png)

Titles can also be placed “outside” the plot area, with default spacing intending to be placed outside the frame:
```
sky.sankey(data,
    titles = [“Summer”,”Winter”],
    frame_side = “both”,
    title_loc = “outer”,
)
```
![Image with options](iface_fruits_titles_outer.png)


## Fonts

The font family, font colour, and font size can be set globally:
```
sky.sankey(data,
    titles=[“Summer”, “Winter”],
    fontsize=15,
    fontfamily=“serif”,
    fontcolor=“red”,
)
```
![Image with options](iface_fruits_fonts.png)

These options do not use `snake_case` for consistency with their underlying Matplotlib options.
Further font options can be passed through directly via the `label_font`, `title_font`, and `value_font` options, which override the settings above.

For example:
```
sky.sankey(
  data3,
  titles    = [“Stage 0”,”Stage 1”,”Stage 2”],
  title_font = {
      “color”: “red”, 
      “fontsize”: 14, 
      “fontweight”: “bold”,
  },
  label_font = {“color”: “blue”},
  value_font = {“color”: “green”},
)
```
![Image with options](iface_data3_fonts_fancy.png)

Refer to [Matplotlib documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html) for available options.





## Frames

Horizontal framing can be placed `”top”`, `”bottom”`, or `”both”`: 
```
sky.sankey(data,frame_side = “both”)
```
![Image with options](iface_fruits_frame.png)

The frame can be coloured:
```
sky.sankey(data,
    frame_side=“both”,
    frame_color=“#62dcbe”,
 )
```
![Image with options](iface_fruits_frame_color.png)


## Edges

Lines around the edges of the nodes and/or flows, and their linewidths (`lw`) can be specified as follows. 
```
sky.sankey(data3,
    node_edge = True,
    flow_edge = True,
    node_lw = 2,
    flow_lw = 1,
    # just for better visuals in this case:
    node_width = 0.1,
    node_alpha = 0.6,
    flow_alpha = 0.3,
    )
```
![Image with options](iface_frame3_edge.png)


## Spacing

A number of parameters can be set to customise the spacing and layout of the diagram. These parameters are normalised against the diagram height or width according to which direction they are oriented. 
```
sky.sankey( data,
            titles = [“Summer”,”Winter”],
            title_side  = “both”,
            frame_side  = “both”,
            sort        = “top”,
            valign      = “center”,
            # spacing parameters:
            node_gap     = 0.01 ,
            node_width   = 0.1 ,
            frame_gap   = 0.2 ,
            label_width = 0.3 ,
            label_gap   = 0.02,
            value_gap   = 0.03,
            title_gap   = 0.1 ,
          )
```
![Image with options](iface_fruits_spacing.png)
