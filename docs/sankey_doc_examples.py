import matplotlib.pyplot as plt
import pandas as pd

import ausankey as sky

data = pd.DataFrame(
    [
        ("apple", 100, "apple", 50),
        ("banana", 200, "banana", 30),
        ("lime", 50, "lime", 20),
        ("blueberry", 20, "blueberry", 10),
        ("orange", 150, "orange", 150),
    ]
)

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

plt.figure()
sky.sankey(data)
plt.show()
plt.savefig("iface_fruits_default.png")
plt.close()

plt.figure()
sky.sankey(data, colormap="jet")
plt.show()
plt.savefig("iface_fruits_jet.png")
plt.close()

color_dict = {"apple": "#f71b1b", "blueberry": "#1b7ef7", "banana": "#f3f71b", "lime": "#12e23f", "orange": "#f78c1b"}

plt.figure()
sky.sankey(data, color_dict=color_dict)
plt.show()
plt.savefig("iface_fruits_colordict.png")
plt.close()

label_dict = {"apple": "Apple", "blueberry": "B'berry", "banana": "Banana", "lime": "Lime", "orange": "Orange"}

plt.figure()
sky.sankey(data, label_dict=label_dict)
plt.show()
plt.savefig("iface_fruits_labeldict.png")
plt.close()


plt.figure()
sky.sankey(data, flow_alpha=0.3)
plt.show()
plt.savefig("iface_fruits_alpha.png")
plt.close()

plt.figure()
sky.sankey(data, sort="top")
plt.show()
plt.savefig("iface_fruits_sort_top.png")
plt.close()

plt.figure()
sky.sankey(data, sort="bottom")
plt.show()
plt.savefig("iface_fruits_sort_bot.png")
plt.close()

plt.figure()
sky.sankey(data, sort="none")
plt.show()
plt.savefig("iface_fruits_sort_none.png")
plt.close()

plt.figure()
sky.sankey(data, titles=["Summer", "Winter"])
plt.show()
plt.savefig("iface_fruits_titles.png")
plt.close()

plt.figure()
sky.sankey(
    data,
    titles=["Summer", "Winter"],
    title_side="bottom",
)
plt.show()
plt.savefig("iface_fruits_titles_bottom.png")
plt.close()

plt.figure()
sky.sankey(data,
    titles = ["Summer","Winter"],
    frame_side = "both",
    title_loc = "outer",
)
plt.show()
plt.savefig("iface_fruits_titles_outer.png")
plt.close()

plt.figure()
sky.sankey(data,
    titles=["Summer", "Winter"],
    fontsize=15,
    fontfamily="serif",
    fontcolor="red",
)
plt.show()
plt.savefig("iface_fruits_fonts.png")
plt.close()

plt.figure(dpi=600)
sky.sankey(
  data3,
  titles    = ["Stage 0","Stage 1","Stage 2"],
  title_font = {
      "color": "red", 
      "fontsize": 14, 
      "fontweight": "bold",
  },
  label_font = {"color": "blue"},
  value_font = {"color": "green"},
)
plt.show()
plt.savefig("iface_data3_fonts_fancy.png")
plt.close()

plt.figure()
sky.sankey(data, valign="center")
plt.show()
plt.savefig("iface_fruits_valign.png")
plt.close()

plt.figure()
sky.sankey(data, frame_side="both")
plt.show()
plt.savefig("iface_fruits_frame.png")
plt.close()

plt.figure()
sky.sankey(data,
    frame_side="both",
    frame_color="#62dcbe",
)
plt.show()
plt.savefig("iface_fruits_frame_color.png")
plt.close()

plt.figure()
sky.sankey(
    data,
    titles=["Summer", "Winter"],
    title_side="both",
    frame_side="both",
    sort="top",
    valign="center",
    # spacing parameters:
    node_gap=0.01,
    node_width=0.1,
    frame_gap=0.2,
    label_width=0.3,
    label_gap=0.02,
    title_gap=0.1,
)
plt.show()
plt.savefig("iface_fruits_spacing.png")
plt.close()

plt.figure()
sky.sankey(
    data,
    node_gap = 0.2,
    label_values = True,
    value_format = "0.1f"
)
plt.show()
plt.savefig("iface_fruits_node_labels.png")
plt.close()

plt.figure()
sky.sankey(
    data,
    label_loc=["right","right","left"],
    label_path_effects = {
        foreground: "black"
    },
    fontcolor = "white" ,
)
plt.show()
plt.savefig("iface_fruits_labels_outline.png")
plt.close()

plt.figure()
sky.sankey(
    data,
    value_loc = ["both","both","both"],
    value_duplicate = False,
)
plt.show()
plt.savefig("iface_fruits_value_dup.png")
plt.close()

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
sky.sankey(data, sort="top", colormap="jet")
plt.savefig("iface_frame2_sort_n1.png")
plt.close()

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

plt.figure(dpi=600)
sky.sankey(
    data3,
    sort="bottom",
    titles=["Stage 1", "Stage 2", "Stage 3"],
    valign="center",
)
plt.savefig("iface_frame3_pretty.png")
plt.close()

plt.figure(dpi=600)
sky.sankey(
    data3,
    label_loc=["right","right","left"],
    value_loc=["none","none","none"],
)
plt.savefig("iface_frame3_labels.png")
plt.close()

plt.figure(dpi=600)
sky.sankey(
    data3,
    label_loc=["right","right","left"],
    value_loc=["none","none","none"],
    label_duplicate=False,
)
plt.savefig("iface_frame3_labels_dup.png")
plt.close()



plt.figure(dpi=600)

sky.sankey(
    data3,
    sort="top",
    color_dict=color_dict,
    label_width=0.1,
    label_gap=0.02,
    node_width=0.05,
    node_gap=0.02,
    flow_alpha=0.3,
    titles=["Stage 1", "Stage 2", "Stage 3"],
    title_gap=0.05,
    title_side="both",
    frame_side="both",
    frame_gap=0.1,
    valign="top",
)

plt.savefig("iface_frame3_many.png")
plt.close()

plt.figure(dpi=600)
sky.sankey(data3,
    node_width = 0.1,
    node_alpha = 0.6,
    flow_alpha = 0.3,
    node_edge = True,
    flow_edge = True,
    node_lw = 2,
    flow_lw = 1,
    )
plt.savefig("iface_frame3_edge.png")
plt.close()





