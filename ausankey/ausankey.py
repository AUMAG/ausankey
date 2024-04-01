"""
Produces simple Sankey Diagrams with matplotlib.

@author: wspr

Forked from: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def sankey(data, **kwargs):
    """Make Sankey Diagram

    Parameters
    ----------
    **kwargs : function arguments
        See the Sankey class for complete list of arguments.

    Returns
    -------

    None (yet)
    """

    sky = Sankey(**kwargs)
    sky.setup(data)
    sky.plot_frame()

    # draw each segment
    for ii in range(sky.num_flow):
        sky.subplot(ii)


class SankeyError(Exception):
    pass


class Sankey:
    """Sankey Diagram

    Parameters
    ----------
    data : DataFrame
        pandas dataframe of labels and weights in alternating columns

    ax : Axis
        Matplotlib plot axis to use

    node_edges: bool
        Whether to plot edges around each node.

    node_lw : float
        Linewidth for node edges.

    node_width : float
        Normalised horizontal width of the data bars
        (1.0 = 100% of plot width)

    node_gap : float
        Normalised vertical gap between successive data bars
        (1.0 = 100% of nominal plot height).

    node_alpha : float
        Opacity of the nodes (`0.0` = transparent, `1.0` = opaque).

    color_dict : dict
        Dictionary of colors to use for each label `{'label': 'color'}`

    colormap : str
        Matplotlib colormap name to automatically assign colours.
        `color_dict` can overide these on an individual basis if needed

    fontsize : int
        Font size of the node labels and titles. Passed through to Matplotlib's text
        option `fontsize`.

    fontfamily: str
        Font family of the node labels and titles. Passed through to Matplotlib's text
        option `fontfamily`.

    fontcolor: color
        Font colour of the node labels and titles. Passed through to Matplotlib's text
        option `color`.

    flow_edge : bool
        Whether to draw an edge to the flows.
        Doesn't always look great when there is lots of branching and overlap.

    flow_lw : float
        Linewidth for flow edges.

    flow_alpha : float
        Opacity of the flows (`0.0` = transparent, `1.0` = opaque)

    frame_side : str
        Whether to place a frame (horizontal rule) above or below the plot.
        Allowed values: `"none"`, `"top"`, `"bottom"`, or `"both"`

    frame_gap : str
        Normalised vertical gap between the top/bottom of the plot and the frame
        (1.0 = 100% of plot height)

    frame_color : color
        Color of frame

    label_dict : dict
        Dictionary of labels to optionally replace the labels in the data
        (e.g., to provide abbreviations or human readable alternatives).
        Format: `{'orig_label': 'printed_label'}`

    label_width : float
        Normalised horizontal space to reserve outside the plot
        on the left and the right for labels
        (1.0 = 100% of plot width)

    label_gap : float
        Normalised horizontal gap between the left/right of the
        plot edges and the label
        (1.0 = 100% of plot width)

    label_loc : [str1, str2, str3]
        Position to place labels next to the nodes.

        * `str1`: position of first labels (`"left"`, `"right"`, `"center"`, or `"none"`)
        * `str2`: position of middle labels (`"left"`, `"right"`, `"both"`, `"center"`, or `"none"`)
        * `str3`: position of last labels (`"left"`, `"right"`, `"center"`, or `"none"`)

    label_duplicate : bool
        When set False, will only print a middle label if that label didn't
        appear in the previous stage. This minimises chart clutter but might
        be confusing in cases, hence defaulting to True.

    other_thresh_val : float
        Sets threshold to recategorise nodes that are below a certain value.
        Up to three dictionary keys can be set:

        * `"val": v` — set node to other if it is less than `v`
        * `"sum": s` — set node to other if it is less than `s` fraction
                       of the summed total of all nodes in the current stage
        * `"max": m` — set node to other if is is less than `m` fraction
                       of the maximum node in the current stage

        If any of these criteria are met the reclassification will occur.

    other_thresh_sum : float
        Sets threshold to recategorise nodes that are below a certain value.
        Up to three dictionary keys can be set:

        * `"val": v` — set node to other if it is less than `v`
        * `"sum": s` — set node to other if it is less than `s` fraction
                       of the summed total of all nodes in the current stage
        * `"max": m` — set node to other if is is less than `m` fraction
                       of the maximum node in the current stage

        If any of these criteria are met the reclassification will occur.

    other_thresh_max : float
        Sets threshold to recategorise nodes that are below a certain value.
        Up to three dictionary keys can be set:

        * `"val": v` — set node to other if it is less than `v`
        * `"sum": s` — set node to other if it is less than `s` fraction
                       of the summed total of all nodes in the current stage
        * `"max": m` — set node to other if is is less than `m` fraction
                       of the maximum node in the current stage

        If any of these criteria are met the reclassification will occur.

    other_name : str
        The string used to rename nodes to if they are classified as “other”.

    sort : int
        Sorting routine to use for the data.
        * `"top"`: data is sorted with largest entries on top
        * `"bottom"`: data is sorted with largest entries on bottom
        * `"none"`: data is presented in the same order as it (first) appears in the DataFrame

    titles : list of str
        Array of title strings for each columns

    title_gap : float
        Normalised vertical gap between the column and the title string
        (1.0 = 100% of plot height)

    title_side : str
        Whether to place the titles above or below the plot.
        Allowed values: `"top"`, `"bottom"`, or `"both"`

    title_loc : str
        Whether to place the titles next to each node of the plot
        or outside the frame.
        Allowed values: `"inner"` or `"outer"`

    valign : str
        Vertical alignment of the data bars at each stage,
        with respect to the whole plot.
        Allowed values: `"top"`, `"bottom"`, or `"center"`"""

    def __init__(
        self,
        ax=None,
        node_width=0.02,
        node_gap=0.05,
        node_alpha=1,
        node_edge=None,
        color_dict=None,
        colormap="viridis",
        flow_edge=None,
        flow_alpha=0.6,
        fontcolor="black",
        fontfamily="sans-serif",
        fontsize=12,
        frame_side="none",
        frame_gap=0.1,
        frame_color=None,
        label_dict=None,
        label_width=0,
        label_gap=0.02,
        label_loc=("left", "none", "right"),
        label_font=None,
        label_duplicate=None,
        flow_lw=1,
        node_lw=1,
        frame_lw=1,
        other_thresh_val=0,
        other_thresh_max=0,
        other_thresh_sum=0,
        other_name="Other",
        titles=None,
        title_gap=0.05,
        title_side="top",  # "bottom", "both"
        title_loc="inner",  # "outer"
        title_font=None,
        sort="bottom",  # "top", "bottom", "none"
        valign="bottom",  # "top","center"
        value_format=".0f",
        value_gap=None,
        value_font=None,
        value_loc=("both", "right", "right"),
        value_thresh_val=0,
        value_thresh_sum=0,
        value_thresh_max=0,
    ):
        self.ax = ax
        self.node_width = node_width
        self.node_gap = node_gap
        self.node_alpha = node_alpha
        self.node_edge = node_edge or False
        self.color_dict = color_dict or {}
        self.colormap = colormap
        self.flow_edge = flow_edge or False
        self.flow_alpha = flow_alpha
        self.fontcolor = fontcolor
        self.fontsize = fontsize
        self.fontfamily = fontfamily
        self.frame_side = frame_side
        self.frame_gap = frame_gap
        self.frame_color = frame_color
        self.label_dict = label_dict or {}
        self.label_width = label_width
        self.label_gap = label_gap
        self.label_loc = label_loc
        self.label_font = label_font or {}
        self.label_duplicate = True if label_duplicate is None else label_duplicate
        self.flow_lw = flow_lw
        self.node_lw = node_lw
        self.frame_lw = frame_lw
        self.other_name = other_name
        self.other_thresh_val = other_thresh_val
        self.other_thresh_max = other_thresh_max
        self.other_thresh_sum = other_thresh_sum
        self.titles = titles
        self.title_font = title_font or {"fontweight": "bold"}
        self.title_gap = title_gap
        self.title_loc = title_loc
        self.title_side = title_side
        self.sort = sort
        self.valign = valign
        self.value_format = value_format
        self.value_gap = label_gap if value_gap is None else value_gap
        self.value_font = value_font or {}
        self.value_loc = value_loc
        self.value_thresh_val = value_thresh_val
        self.value_thresh_sum = value_thresh_sum
        self.value_thresh_max = value_thresh_max

    def setup(self, data):
        self.data = data

        num_col = len(self.data.columns)
        self.data.columns = range(num_col)  # force numeric column headings
        self.num_stages = int(num_col / 2)  # number of stages
        self.num_flow = self.num_stages - 1

        # sizes
        col_hgt = np.empty(self.num_stages)
        self.node_sizes = {}
        self.nodes_uniq = {}

        # weight and reclassify
        self.weight_labels()
        for ii in range(self.num_stages):
            for nn, lbl in enumerate(self.data[2 * ii]):
                val = self.node_sizes[ii][lbl]
                if lbl is not None and (
                    val < self.other_thresh_val
                    or val < self.other_thresh_sum * self.weight_sum[ii]
                    or val < self.other_thresh_max * max(self.data[2 * ii + 1])
                ):
                    self.data.iat[nn, 2 * ii] = self.other_name
        self.weight_labels()

        # sort and calc
        self.plot_height_nom = max(self.weight_sum)
        for ii in range(self.num_stages):
            self.node_sizes[ii] = sort_dict(self.node_sizes[ii], self.sort)
            col_hgt[ii] = self.weight_sum[ii] + (len(self.nodes_uniq[ii]) - 1) * self.node_gap * self.plot_height_nom

        # overall dimensions
        self.plot_height = max(col_hgt)
        self.sub_width = self.plot_height
        self.plot_width = (
            (self.num_stages - 1) * self.sub_width
            + 2 * self.sub_width * (self.label_gap + self.label_width)
            + self.num_stages * self.sub_width * self.node_width
        )

        # offsets for alignment
        vscale_dict = {"top": 1, "center": 0.5, "bottom": 0}
        self.vscale = vscale_dict.get(self.valign, 0)
        self.voffset = np.empty(self.num_stages)
        for ii in range(self.num_stages):
            self.voffset[ii] = self.vscale * (col_hgt[1] - col_hgt[ii])

        # labels
        label_record = self.data[range(0, 2 * self.num_stages, 2)].to_records(index=False)
        flattened = [item for sublist in label_record for item in sublist]
        self.all_labels = pd.Series(flattened).unique()

        # If no color_dict given, make one
        color_dict_new = {}
        cmap = plt.cm.get_cmap(self.colormap)
        color_palette = cmap(np.linspace(0, 1, len(self.all_labels)))
        for i, label in enumerate(self.all_labels):
            color_dict_new[label] = self.color_dict.get(label, color_palette[i])
        # check_colors_match_labels(self.all_labels, color_dict_new)
        self.color_dict = color_dict_new

        # initialise plot
        self.ax = self.ax or plt.gca()
        self.ax.axis("off")

    def weight_labels(self):
        self.weight_sum = np.empty(self.num_stages)

        for ii in range(self.num_stages):
            self.nodes_uniq[ii] = pd.Series(self.data[2 * ii]).unique()

        for ii in range(self.num_stages):
            self.node_sizes[ii] = {}
            for lbl in self.nodes_uniq[ii]:
                if ii == 0:
                    ind_prev = self.data[2 * ii - 0] == lbl
                    ind_this = self.data[2 * ii + 0] == lbl
                    ind_next = self.data[2 * ii + 2] == lbl
                elif ii == self.num_flow:
                    ind_prev = self.data[2 * ii - 2] == lbl
                    ind_this = self.data[2 * ii + 0] == lbl
                    ind_next = self.data[2 * ii + 0] == lbl
                else:
                    ind_prev = self.data[2 * ii - 2] == lbl
                    ind_this = self.data[2 * ii + 0] == lbl
                    ind_next = self.data[2 * ii + 2] == lbl
                weight_cont = self.data[2 * ii + 1][ind_this & ind_prev & ind_next].sum()
                weight_only = self.data[2 * ii + 1][ind_this & ~ind_prev & ~ind_next].sum()
                weight_stop = self.data[2 * ii + 1][ind_this & ind_prev & ~ind_next].sum()
                weight_strt = self.data[2 * ii + 1][ind_this & ~ind_prev & ind_next].sum()
                self.node_sizes[ii][lbl] = weight_cont + weight_only + max(weight_stop, weight_strt)

            self.weight_sum[ii] = pd.Series(self.node_sizes[ii].values()).sum()

    def plot_frame(self):
        """Plot frame on top/bottom edges"""

        frame_top = self.frame_side in ("top", "both")
        frame_bot = self.frame_side in ("bottom", "both")

        frame_color = self.frame_color or [0, 0, 0, 1]

        y_frame_gap = self.frame_gap * self.plot_height

        col = frame_color if frame_top else [1, 1, 1, 0]
        self.ax.plot(
            [0, self.plot_width],
            min(self.voffset) + (self.plot_height) + y_frame_gap + [0, 0],
            color=col,
            lw=self.frame_lw,
        )

        col = frame_color if frame_bot else [1, 1, 1, 0]
        self.ax.plot(
            [0, self.plot_width],
            min(self.voffset) - y_frame_gap + [0, 0],
            color=col,
            lw=self.frame_lw,
        )

    def subplot(self, ii):
        """Subroutine for plotting horizontal sections of the Sankey plot

        Some special-casing is used for plotting/labelling differently
        for the first and last cases.
        """

        labelind = 2 * ii
        weightind = 2 * ii + 1

        lastind = 4 if ii < self.num_flow - 1 else 2
        labels_lr = [
            self.data[labelind],
            self.data[labelind + 2],
            self.data[labelind + lastind],
        ]
        weights_lr = [
            self.data[weightind],
            self.data[weightind + 2],
            self.data[weightind + lastind],
        ]

        nodes_lr = [
            sort_nodes(labels_lr[0], self.node_sizes[ii]),
            sort_nodes(labels_lr[1], self.node_sizes[ii + 1]),
        ]

        # Determine sizes of individual subflows
        nodesize = [{}, {}]
        for lbl_l in nodes_lr[0]:
            nodesize[0][lbl_l] = {}
            nodesize[1][lbl_l] = {}
            for lbl_r in nodes_lr[1]:
                ind = (labels_lr[0] == lbl_l) & (labels_lr[1] == lbl_r)
                nodesize[0][lbl_l][lbl_r] = weights_lr[0][ind].sum()
                nodesize[1][lbl_l][lbl_r] = weights_lr[1][ind].sum()

        # Determine vertical positions of nodes
        y_node_gap = self.node_gap * self.plot_height_nom

        node_voffset = [{}, {}]
        node_pos_bot = [{}, {}]
        node_pos_top = [{}, {}]

        for lr in [0, 1]:
            for i, label in enumerate(nodes_lr[lr]):
                node_height = self.node_sizes[ii + lr][label]
                this_side_height = weights_lr[lr][labels_lr[lr] == label].sum()
                node_voffset[lr][label] = self.vscale * (node_height - this_side_height)
                next_bot = node_pos_top[lr][nodes_lr[lr][i - 1]] + y_node_gap if i > 0 else 0
                node_pos_bot[lr][label] = self.voffset[ii + lr] if i == 0 else next_bot
                node_pos_top[lr][label] = node_pos_bot[lr][label] + node_height

        # horizontal positions of nodes
        x_node_width = self.node_width * self.sub_width
        x_label_width = self.label_width * self.sub_width
        x_label_gap = self.label_gap * self.sub_width
        x_value_gap = self.value_gap * self.sub_width
        x_left = x_node_width + x_label_gap + x_label_width + ii * (self.sub_width + x_node_width)
        x_lr = [x_left, x_left + self.sub_width]

        # Draw nodes

        def draw_node(x, dx, y, dy, label):
            edge_lw = self.node_lw if self.node_edge else 0
            self.ax.fill_between(
                [x, x + dx],
                y,
                y + dy,
                facecolor=self.color_dict[label],
                alpha=self.node_alpha,
                lw=edge_lw,
                snap=True,
            )
            if self.node_edge:
                self.ax.fill_between(
                    [x, x + dx],
                    y,
                    y + dy,
                    edgecolor=self.color_dict[label],
                    facecolor="none",
                    lw=edge_lw,
                    snap=True,
                )

        for lr in [0, 1] if ii == 0 else [1]:
            for label in nodes_lr[lr]:
                draw_node(
                    x_lr[lr] - x_node_width * (1 - lr),
                    x_node_width,
                    node_pos_bot[lr][label],
                    self.node_sizes[ii + lr][label],
                    label,
                )

        # Draw node labels

        def draw_label(x, y, label, ha):
            self.ax.text(
                x,
                y,
                self.label_dict.get(label, label),
                {
                    "ha": ha,
                    "va": "center",
                    "fontfamily": self.fontfamily,
                    "fontsize": self.fontsize,
                    "color": self.fontcolor,
                    **self.label_font,
                },
            )

        ha_dict = {"left": "right", "right": "left", "center": "center"}

        # first row of labels
        lr = 0
        if ii == 0 and self.label_loc[0] != "none":
            if self.label_loc[0] in ("left"):
                xx = x_lr[lr] - x_label_gap - x_node_width
            elif self.label_loc[0] in ("right"):
                xx = x_lr[lr] + x_label_gap
            elif self.label_loc[0] in ("center"):
                xx = x_lr[lr] - x_node_width / 2
            for label in nodes_lr[lr]:
                yy = node_pos_bot[lr][label] + self.node_sizes[ii + lr][label] / 2
                draw_label(xx, yy, label, ha_dict[self.label_loc[0]])

        # inside labels, left
        lr = 1
        if ii < self.num_flow - 1 and self.label_loc[1] in ("left", "both"):
            xx = x_lr[lr] - x_label_gap
            ha = "right"
            for label in nodes_lr[lr]:
                if (label not in nodes_lr[lr - 1]) or self.label_duplicate:
                    yy = node_pos_bot[lr][label] + self.node_sizes[ii + lr][label] / 2
                    draw_label(xx, yy, label, ha)

        # inside labels, center
        if ii < self.num_flow - 1 and self.label_loc[1] in ("center"):
            xx = x_lr[lr] + x_node_width / 2
            ha = "center"
            for label in nodes_lr[lr]:
                if (label not in nodes_lr[lr - 1]) or self.label_duplicate:
                    yy = node_pos_bot[lr][label] + self.node_sizes[ii + lr][label] / 2
                    draw_label(xx, yy, label, ha)

        # inside labels, right
        if ii < self.num_flow - 1 and self.label_loc[1] in ("right", "both"):
            xx = x_lr[lr] + x_label_gap + x_node_width
            ha = "left"
            for label in nodes_lr[lr]:
                if (label not in nodes_lr[lr - 1]) or self.label_duplicate:
                    yy = node_pos_bot[lr][label] + self.node_sizes[ii + lr][label] / 2
                    draw_label(xx, yy, label, ha)

        # last row of labels
        if ii == self.num_flow - 1 and self.label_loc[2] != "none":
            if self.label_loc[2] in ("left"):
                xx = x_lr[lr] - x_label_gap
            elif self.label_loc[2] in ("right"):
                xx = x_lr[lr] + x_label_gap + x_node_width
            elif self.label_loc[2] in ("center"):
                xx = x_lr[lr] + x_node_width / 2
            for label in nodes_lr[lr]:
                yy = node_pos_bot[lr][label] + self.node_sizes[ii + lr][label] / 2
                draw_label(xx, yy, label, ha_dict[self.label_loc[2]])

        # Plot flows
        if self.flow_edge:
            edge_lw = self.flow_lw
            edge_alpha = 1
        else:
            edge_alpha = self.flow_alpha
            edge_lw = 0

        for lbl_l in nodes_lr[0]:
            for lbl_r in nodes_lr[1]:
                lind = labels_lr[0] == lbl_l
                rind = labels_lr[1] == lbl_r
                if not any(lind & rind):
                    continue

                lbot = node_voffset[0][lbl_l] + node_pos_bot[0][lbl_l]
                rbot = node_voffset[1][lbl_r] + node_pos_bot[1][lbl_r]
                llen = nodesize[0][lbl_l][lbl_r]
                rlen = nodesize[1][lbl_l][lbl_r]
                bot_lr = [lbot, rbot]
                len_lr = [llen, rlen]

                ys_d = create_curve(lbot, rbot)
                ys_u = create_curve(lbot + llen, rbot + rlen)

                # Update bottom edges at each label
                # so next strip starts at the right place
                node_pos_bot[0][lbl_l] += llen
                node_pos_bot[1][lbl_r] += rlen

                xx = np.linspace(x_lr[0], x_lr[1], len(ys_d))
                cc = combine_colours(self.color_dict[lbl_l], self.color_dict[lbl_r], len(ys_d))

                for jj in range(len(ys_d) - 1):
                    self.ax.fill_between(
                        xx[[jj, jj + 1]],
                        ys_d[[jj, jj + 1]],
                        ys_u[[jj, jj + 1]],
                        color=cc[:, jj],
                        alpha=self.flow_alpha,
                        lw=0,
                        edgecolor="none",
                        snap=True,
                    )
                    # edges:
                    self.ax.plot(
                        xx[[jj, jj + 1]],
                        ys_d[[jj, jj + 1]],
                        color=cc[:, jj],
                        alpha=edge_alpha,
                        lw=edge_lw,
                        snap=True,
                    )
                    self.ax.plot(
                        xx[[jj, jj + 1]],
                        ys_u[[jj, jj + 1]],
                        color=cc[:, jj],
                        alpha=edge_alpha,
                        lw=edge_lw,
                        snap=True,
                    )

                ha = ["left", "right"]
                sides = []
                if ii == 0:
                    ind = 0
                elif ii == self.num_flow - 1:
                    ind = 2
                else:
                    ind = 1
                if self.value_loc[ind] in ("left", "both"):
                    sides.append(0)
                if self.value_loc[ind] in ("right", "both"):
                    sides.append(1)
                for lr in sides:
                    val = len_lr[lr]
                    if (
                        val < self.value_thresh_val
                        or val < self.value_thresh_sum * self.weight_sum[ii + lr]
                        or val < self.value_thresh_max * max(self.data[2 * ii + 1])
                    ):
                        continue
                    self.ax.text(
                        x_lr[lr] + (1 - 2 * lr) * x_value_gap,
                        bot_lr[lr] + len_lr[lr] / 2,
                        f"{format(val,self.value_format)}",
                        ha=ha[lr],
                        va="center",
                        **self.value_font,
                    )

        # Place "titles"
        if self.titles is not None:
            last_label = [lbl_l, lbl_r]

            y_title_gap = self.title_gap * self.plot_height_nom
            y_frame_gap = self.frame_gap * self.plot_height_nom

            title_x = [
                x_lr[0] - x_node_width / 2,
                x_lr[1] + x_node_width / 2,
            ]

            def draw_title(x, y, label, va):
                self.ax.text(
                    x,
                    y,
                    label,
                    {
                        "ha": "center",
                        "va": va,
                        "fontfamily": self.fontfamily,
                        "fontsize": self.fontsize,
                        "color": self.fontcolor,
                        **self.title_font,
                    },
                )

            # leftmost title
            title_lr = [0, 1] if ii == 0 else [1]

            for lr in title_lr:
                if self.title_side in ("top", "both"):
                    if self.title_loc == "outer":
                        yt = min(self.voffset) + y_title_gap + y_frame_gap + self.plot_height
                    elif self.title_loc == "inner":
                        yt = y_title_gap + node_pos_top[lr][last_label[lr]]
                    draw_title(title_x[lr], yt, self.titles[ii + lr], "bottom")

                if self.title_side in ("bottom", "both"):
                    if self.title_loc == "outer":
                        yt = min(self.voffset) - y_title_gap - y_frame_gap
                    elif self.title_loc == "inner":
                        yt = self.voffset[ii + lr] - y_title_gap
                    draw_title(title_x[lr], yt, self.titles[ii + lr], "top")


###########################################


def sort_nodes(lbl, node_sizes):
    """creates a sorted list of labels by their summed weights"""

    arr = {}
    for uniq in lbl.unique():
        if uniq is not None:
            arr[uniq] = True

    sort_arr = sorted(
        arr.items(),
        key=lambda item: list(node_sizes).index(item[0]),
        # sorting = 0,1,-1 affects this
    )

    return list(dict(sort_arr).keys())


###########################################


def sort_dict(lbl, sorting):
    """creates a sorted list of labels by their summed weights"""

    if sorting == "top":
        s = 1
    elif sorting == "bottom":
        s = -1
    elif sorting == "center":
        s = 1
    else:
        s = 0

    sort_arr = sorted(
        lbl.items(),
        key=lambda item: s * item[1],
        # sorting = 0,1,-1 affects this
    )

    sorted_labels = dict(sort_arr)

    if sorting == "center":
        # this kinda works but i dont think it's a good idea because you lose perception of relative sizes
        # probably has an off-by-one even/odd error
        sorted_labels = sorted_labels[1::2] + sorted_labels[-1::-2]

    return sorted_labels


###########################################


def check_colors_match_labels(labels_lr, color_dict):
    """Check that all labels in labels_lr are in color_dict"""

    all_labels = pd.Series([*labels_lr[0], *labels_lr[1]]).unique()

    missing = [label for label in all_labels if label not in color_dict]

    if missing:
        msg = "The color_dict parameter is missing " "values for the following labels: "
        msg += "{}".format(", ".join(missing))
        raise ValueError(msg)


###########################################


def create_curve(lpoint, rpoint):
    """Create array of y values for each strip"""

    num_div = 20
    num_arr = 50

    # half at left value, half at right, convolve

    ys = np.array(num_arr * [lpoint] + num_arr * [rpoint])

    ys = np.convolve(ys, 1 / num_div * np.ones(num_div), mode="valid")

    return np.convolve(ys, 1 / num_div * np.ones(num_div), mode="valid")


###########################################


def combine_colours(c1, c2, num_col):
    """Creates N colours needed to produce a gradient

    Parameters
    ----------

    c1 : col
        First (left) colour. Can be a colour string `"#rrbbgg"` or a colour list `[r, b, g, a]`

    c1 : col
        Second (right) colour. As above.

    num_col : int
        The number of colours N to create in the array.

    Returns
    -------

    color_array : np.array
        4xN array of numerical colours
    """
    color_array_len = 4
    # if not [r,g,b,a] assume a hex string like "#rrggbb":

    if len(c1) != color_array_len:
        r1 = int(c1[1:3], 16) / 255
        g1 = int(c1[3:5], 16) / 255
        b1 = int(c1[5:7], 16) / 255
        c1 = [r1, g1, b1, 1]

    if len(c2) != color_array_len:
        r2 = int(c2[1:3], 16) / 255
        g2 = int(c2[3:5], 16) / 255
        b2 = int(c2[5:7], 16) / 255
        c2 = [r2, g2, b2, 1]

    rr = np.linspace(c1[0], c2[0], num_col)
    gg = np.linspace(c1[1], c2[1], num_col)
    bb = np.linspace(c1[2], c2[2], num_col)
    aa = np.linspace(c1[3], c2[3], num_col)

    return np.array([rr, gg, bb, aa])
