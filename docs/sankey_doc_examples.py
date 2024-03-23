import matplotlib.pyplot as plt
import pandas as pd

import ausankey as sky

data = pd.read_csv("../tests/fruit.csv")

plt.figure()
sky.sankey(data)
plt.show()
plt.savefig("fruits_default.png")

data = pd.DataFrame(
    [
        ("apple", 1, "apple", 0.5),
        ("banana", 2, "banana", 3),
        ("lime", 0.5, "lime", 0.2),
        ("blueberry", 0.2, "blueberry", 1),
        ("orange", 1.5, "orange", 1.5),
    ]
)

plt.figure()
sky.sankey(data, colormap="jet")
plt.show()
plt.savefig("fruits_jet.png")

color_dict = {"apple": "#f71b1b", "blueberry": "#1b7ef7", "banana": "#f3f71b", "lime": "#12e23f", "orange": "#f78c1b"}

plt.figure()
sky.sankey(data, color_dict=color_dict)
plt.show()
plt.savefig("fruits_colordict.png")

label_dict = {"apple": "Apple", "blueberry": "B'berry", "banana": "Banana", "lime": "Lime", "orange": "Orange"}

plt.figure()
sky.sankey(data, label_dict=label_dict)
plt.show()
plt.savefig("fruits_labeldict.png")

plt.figure()
sky.sankey(data, alpha=0.3)
plt.show()
plt.savefig("fruits_alpha.png")

plt.figure()
sky.sankey(data, sort="top")
plt.show()
plt.savefig("fruits_sort_top.png")

plt.figure()
sky.sankey(data, sort="bottom")
plt.show()
plt.savefig("fruits_sort_bot.png")

plt.figure()
sky.sankey(data, sort="none")
plt.show()
plt.savefig("fruits_sort_none.png")

plt.figure()
sky.sankey(data, titles=["Summer", "Winter"])
plt.show()
plt.savefig("fruits_titles.png")

plt.figure()
sky.sankey(
    data,
    titles=["Summer", "Winter"],
    title_side="bottom",
)
plt.show()
plt.savefig("fruits_titles_bottom.png")

plt.figure()
sky.sankey(data,
    titles = ["Summer","Winter"],
    frame_side = "both",
    title_loc = "outer",
)
plt.show()
plt.savefig("fruits_titles_outer.png")

plt.figure()
sky.sankey(data, valign="center")
plt.show()
plt.savefig("fruits_valign.png")

plt.figure()
sky.sankey(data, frame_side="both")
plt.show()
plt.savefig("fruits_frame.png")

plt.figure()
sky.sankey(data,
    frame_side="both",
    frame_color="#62dcbe",
 )
plt.show()
plt.savefig("fruits_frame_color.png")

plt.figure()
sky.sankey(
    data,
    titles=["Summer", "Winter"],
    title_side="both",
    frame_side="both",
    sort="top",
    valign="center",
    # spacing parameters:
    bar_gap=0.01,
    bar_width=0.1,
    frame_gap=0.2,
    label_width=0.3,
    label_gap=0.02,
    title_gap=0.1,
)
plt.show()
plt.savefig("fruits_spacing.png")

data = pd.DataFrame(
    [
        ("a", 1.0, "ab", 2.0),
        ("a", 1.0, "ba", 0.8),
        ("c", 1.5, "cd", 0.5),
        ("b", 0.5, "ba", 0.8),
        ("b", 0.5, "ab", 0.8),
        ("d", 2.0, "cd", 0.4),
        ("e", 1.0, "e", 1.0),
    ]
)

plt.figure()
sky.sankey(data, sort="top", colormap="jet", aspect=0.5)
plt.savefig("frame2_sort_n1.png")


color_dict = {
    "a": "#f71b1b",
    "b": "#1b7ef7",
    "ab": "#8821aa",
    "ba": "#6016aa",
    "cd": "#c1e849",
    "c": "#f3f71b",
    "d": "#12e23f",
    "e": "#f78c1b",
}

data = pd.DataFrame(
    [
        ("a", 1.0, "ab", 2.0, "a", 1.0),
        ("a", 1.0, "ba", 0.8, "ba", 0.4),
        ("c", 1.5, "cd", 0.5, "d", 2.0),
        ("b", 0.5, "ba", 0.8, "ba", 0.4),
        ("b", 0.5, "ab", 0.8, "a", 1.0),
        ("d", 2.0, "cd", 0.4, "d", 1.0),
        ("e", 1.0, "e", 1.0, "e", 3.0),
    ]
)

plt.figure(dpi=600)
sky.sankey(
    data,
    sort="bottom",
    titles=["Stage 1", "Stage 2", "Stage 3"],
    valign="center",
)
plt.savefig("frame3_pretty.png")


plt.figure(dpi=600)
sky.sankey(
    data,
    labels_loc=["right","right","left"],
)
plt.savefig("frame3_labels.png")



plt.figure(dpi=600)

sky.sankey(
    data,
    sort="top",
    color_dict=color_dict,
    label_width=0.1,
    label_gap=0.02,
    bar_width=0.05,
    bar_gap=0.02,
    alpha=0.3,
    titles=["Stage 1", "Stage 2", "Stage 3"],
    title_gap=0.05,
    title_side="both",
    frame_side="both",
    frame_gap=0.1,
    valign="top",
)

plt.savefig("frame3_many.png")
