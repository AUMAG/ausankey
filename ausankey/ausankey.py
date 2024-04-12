"""
Produces simple Sankey Diagrams with matplotlib.

@author: wspr

Forked from: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

###########################################


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


###########################################


class SankeyError(Exception):
    pass


###########################################


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

    label_font : dict
        Dictionary of Matplotlib text options to be passed to the labels.

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

    sort_dict : dict
        Override the weight sum used to sort nodes by the value specified in the dict.
        Typically used to force particular categories to the top or bottom.

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

    title_font : dict
        Dictionary of Matplotlib text options to be passed to the titles.

    valign : str
        Vertical alignment of the data bars at each stage,
        with respect to the whole plot.
        Allowed values: `"top"`, `"bottom"`, or `"center"`

    value_loc : dict
        label_loc : [str1, str2, str3]
        Position to place values next to the nodes corresponding to the sizes.
        These are placed within the flows at the beginning (left) and end (right) of each one.
        Each str can be one of: `"left"`, `"right"`, `"both"`, or `"none"`

        * `str1`: position of value(s) in first flow
        * `str2`: position of value(s) in middle flows
        * `str3`: position of value(s) in last flow

    value_format : str
        String formatting specification passed internally to the `format()` function.

    value_gap : float
        Horizontal space fraction between the edge of the node and the value label.
        Defaults to `label_gap`.

    value_font : dict
        Dictionary of Matplotlib text options to be passed to the value labels.

    value_thresh_val : float
        Only print labels larger than this absolute value threshold.

    value_thresh_sum : float
        Only print labels larger than this threshold as a fraction of the sum of all node weights in the stage.

    value_thresh_max : float
        Only print labels larger than this threshold as a fraction of the maximum node weight in the stage."""

    def __init__(
        self,
        ax=None,
        color_dict=None,
        colormap="viridis",
        flow_edge=None,
        flow_alpha=0.6,
        flow_lw=1,
        fontcolor="black",
        fontfamily="sans-serif",
        fontsize=12,
        frame_side="none",
        frame_gap=0.1,
        frame_color=None,
        frame_lw=1,
        label_dict=None,
        label_width=0,
        label_gap=0.02,
        label_loc=("left", "none", "right"),
        label_font=None,
        label_duplicate=None,
        node_lw=1,
        node_width=0.02,
        node_gap=0.05,
        node_alpha=1,
        node_edge=None,
        other_thresh_val=0,
        other_thresh_max=0,
        other_thresh_sum=0,
        other_name="Other",
        sort="bottom",  # "top", "bottom", "none"
        sort_dict=None,
        titles=None,
        title_gap=0.05,
        title_side="top",  # "bottom", "both"
        title_loc="inner",  # "outer"
        title_font=None,
        valign="bottom",  # "top","center"
        value_format=".0f",
        value_gap=None,
        value_font=None,
        value_loc=("both", "right", "right"),
        value_thresh_val=0,
        value_thresh_sum=0,
        value_thresh_max=0,
    ):
        """Assigns all input arguments to the class as variables with appropriate defaults"""
        self.ax = ax
        self.color_dict = color_dict or {}
        self.colormap = colormap
        self.flow_edge = flow_edge or False
        self.flow_alpha = flow_alpha
        self.flow_lw = flow_lw
        self.fontcolor = fontcolor
        self.fontsize = fontsize
        self.fontfamily = fontfamily
        self.frame_side = frame_side
        self.frame_gap = frame_gap
        self.frame_color = frame_color
        self.frame_lw = frame_lw
        self.label_dict = label_dict or {}
        self.label_width = label_width
        self.label_gap = label_gap
        self.label_loc = label_loc
        self.label_font = label_font or {}
        self.label_duplicate = True if label_duplicate is None else label_duplicate
        self.node_lw = node_lw
        self.node_width = node_width
        self.node_gap = node_gap
        self.node_alpha = node_alpha
        self.node_edge = node_edge or False
        self.other_name = other_name
        self.other_thresh_val = other_thresh_val
        self.other_thresh_max = other_thresh_max
        self.other_thresh_sum = other_thresh_sum
        self.sort = sort
        self.sort_dict = sort_dict or {}
        self.titles = titles
        self.title_font = title_font or {"fontweight": "bold"}
        self.title_gap = title_gap
        self.title_loc = title_loc
        self.title_side = title_side
        self.valign = valign
        self.value_format = value_format
        self.value_gap = label_gap if value_gap is None else value_gap
        self.value_font = value_font or {}
        self.value_loc = value_loc
        self.value_thresh_val = value_thresh_val
        self.value_thresh_sum = value_thresh_sum
        self.value_thresh_max = value_thresh_max

    ###########################################

    def setup(self, data):
        """Calculates all parameters needed to plot the graph"""

        self.data = data

        num_col = len(self.data.columns)
        self.data.columns = range(num_col)  # force numeric column headings
        self.num_stages = int(num_col / 2)  # number of stages
        self.num_flow = self.num_stages - 1

        # sizes
        col_hgt = np.empty(self.num_stages)
        self.node_sizes = {}
        self.node_list = {}
        self.nodes_uniq = {}

        self.node_pos_voffset = {}
        self.node_pos_bot = {}
        self.node_pos_top = {}

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
            self.node_sizes[ii] = self.sort_node_sizes(self.node_sizes[ii], self.sort)
            col_hgt[ii] = self.weight_sum[ii] + (len(self.nodes_uniq[ii]) - 1) * self.node_gap * self.plot_height_nom
            self.node_list[ii] = self.sort_nodes(self.data[2 * ii], self.node_sizes[ii])

        # offsets for alignment
        vscale_dict = {"top": 1, "center": 0.5, "bottom": 0}
        self.vscale = vscale_dict.get(self.valign, 0)
        self.voffset = np.empty(self.num_stages)
        for ii in range(self.num_stages):
            self.voffset[ii] = self.vscale * (col_hgt[1] - col_hgt[ii])

        # overall dimensions
        self.plot_height = max(col_hgt)
        self.sub_width = self.plot_height
        self.plot_width_nom = (self.num_stages - 1) * self.sub_width
        self.plot_width = (
            (self.num_stages - 1) * self.sub_width
            + 2 * self.plot_width_nom * (self.label_gap + self.label_width)
            + self.num_stages * self.plot_width_nom * self.node_width
        )

        # vertical positions
        self.y_node_gap = self.node_gap * self.plot_height_nom
        self.y_title_gap = self.title_gap * self.plot_height_nom
        self.y_frame_gap = self.frame_gap * self.plot_height_nom

        # horizontal positions
        self.x_node_width = self.node_width * self.plot_width_nom
        self.x_label_width = self.label_width * self.plot_width_nom
        self.x_label_gap = self.label_gap * self.plot_width_nom
        self.x_value_gap = self.value_gap * self.plot_width_nom

        self.x_lr = {}
        self.nodesize_l = {}
        self.nodesize_r = {}
        self.node_pairs = {}
        for ii in range(self.num_flow):
            x_left = (
                self.x_node_width + self.x_label_gap + self.x_label_width + ii * (self.sub_width + self.x_node_width)
            )
            self.x_lr[ii] = (x_left, x_left + self.sub_width)
            self.nodesize_l[ii] = {}
            self.nodesize_r[ii] = {}
            self.node_pairs[ii] = []
            for lbl_l in self.node_list[ii]:
                self.nodesize_l[ii][lbl_l] = {}
                self.nodesize_r[ii][lbl_l] = {}
                for lbl_r in self.node_list[ii + 1]:
                    ind = (self.data[2 * ii] == lbl_l) & (self.data[2 * ii + 2] == lbl_r)
                    if not any(ind):
                        continue
                    self.node_pairs[ii].append((lbl_l, lbl_r))
                    self.nodesize_l[ii][lbl_l][lbl_r] = self.data[2 * ii + 1][ind].sum()
                    self.nodesize_r[ii][lbl_l][lbl_r] = self.data[2 * ii + 3][ind].sum()

        # All node sizes and positions
        for ii in range(self.num_flow):
            self.node_pos_voffset[ii] = [{}, {}]
            self.node_pos_bot[ii] = [{}, {}]
            self.node_pos_top[ii] = [{}, {}]
            for lr in [0, 1]:
                for i, label in enumerate(self.node_list[ii + lr]):
                    node_height = self.node_sizes[ii + lr][label]
                    this_side_height = self.data[2 * (ii + lr) + 1][self.data[2 * (ii + lr)] == label].sum()
                    self.node_pos_voffset[ii][lr][label] = self.vscale * (node_height - this_side_height)
                    if i == 0:
                        tmp_top = self.voffset[ii + lr]
                    else:
                        tmp_top = self.node_pos_top[ii][lr][self.node_list[ii + lr][i - 1]] + self.y_node_gap
                    self.node_pos_bot[ii][lr][label] = tmp_top
                    self.node_pos_top[ii][lr][label] = self.node_pos_bot[ii][lr][label] + node_height

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

    ###########################################

    def weight_labels(self):
        """Calculates sizes of each node, taking into account discontinuities"""
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

    ###########################################

    def plot_frame(self):
        """Plot frame on top/bottom edges"""

        frame_top = self.frame_side in ("top", "both")
        frame_bot = self.frame_side in ("bottom", "both")

        frame_color = self.frame_color or [0, 0, 0, 1]

        self.y_frame_gap = self.frame_gap * self.plot_height

        col = frame_color if frame_top else [1, 1, 1, 0]
        self.ax.plot(
            [0, self.plot_width],
            min(self.voffset) + (self.plot_height) + self.y_frame_gap + [0, 0],
            color=col,
            lw=self.frame_lw,
        )

        col = frame_color if frame_bot else [1, 1, 1, 0]
        self.ax.plot(
            [0, self.plot_width],
            min(self.voffset) - self.y_frame_gap + [0, 0],
            color=col,
            lw=self.frame_lw,
        )

    ###########################################

    def subplot(self, ii):
        """Subroutine for plotting horizontal sections of the Sankey plot

        Some special-casing is used for plotting/labelling differently
        for the first and last cases.
        """

        # Abbrev

        x_lr = self.x_lr[ii]

        # Draw nodes

        for lr in [0, 1] if ii == 0 else [1]:
            for label in self.node_list[ii + lr]:
                self.draw_node(
                    x_lr[lr] - self.x_node_width * (1 - lr),
                    self.x_node_width,
                    self.node_pos_bot[ii][lr][label],
                    self.node_sizes[ii + lr][label],
                    label,
                )

        # Draw node labels

        ha_dict = {"left": "right", "right": "left", "center": "center"}

        # first row of labels
        lr = 0
        if ii == 0 and self.label_loc[0] != "none":
            if self.label_loc[0] in ("left"):
                xx = x_lr[lr] - self.x_label_gap - self.x_node_width
            elif self.label_loc[0] in ("right"):
                xx = x_lr[lr] + self.x_label_gap
            elif self.label_loc[0] in ("center"):
                xx = x_lr[lr] - self.x_node_width / 2
            for label in self.node_list[ii + lr]:
                yy = self.node_pos_bot[ii][lr][label] + self.node_sizes[ii + lr][label] / 2
                self.draw_label(xx, yy, label, ha_dict[self.label_loc[0]])

        # inside labels, left
        lr = 1
        if ii < self.num_flow - 1 and self.label_loc[1] in ("left", "both"):
            xx = x_lr[lr] - self.x_label_gap
            ha = "right"
            for label in self.node_list[ii + lr]:
                if (label not in self.node_list[ii]) or self.label_duplicate:
                    yy = self.node_pos_bot[ii][lr][label] + self.node_sizes[ii + lr][label] / 2
                    self.draw_label(xx, yy, label, ha)

        # inside labels, center
        if ii < self.num_flow - 1 and self.label_loc[1] in ("center"):
            xx = x_lr[lr] + self.x_node_width / 2
            ha = "center"
            for label in self.node_list[ii + lr]:
                if (label not in self.node_list[ii]) or self.label_duplicate:
                    yy = self.node_pos_bot[ii][lr][label] + self.node_sizes[ii + lr][label] / 2
                    self.draw_label(xx, yy, label, ha)

        # inside labels, right
        if ii < self.num_flow - 1 and self.label_loc[1] in ("right", "both"):
            xx = x_lr[lr] + self.x_label_gap + self.x_node_width
            ha = "left"
            for label in self.node_list[ii + lr]:
                if (label not in self.node_list[ii]) or self.label_duplicate:
                    yy = self.node_pos_bot[ii][lr][label] + self.node_sizes[ii + lr][label] / 2
                    self.draw_label(xx, yy, label, ha)

        # last row of labels
        if ii == self.num_flow - 1 and self.label_loc[2] != "none":
            if self.label_loc[2] in ("left"):
                xx = x_lr[lr] - self.x_label_gap
            elif self.label_loc[2] in ("right"):
                xx = x_lr[lr] + self.x_label_gap + self.x_node_width
            elif self.label_loc[2] in ("center"):
                xx = x_lr[lr] + self.x_node_width / 2
            for label in self.node_list[ii + lr]:
                yy = self.node_pos_bot[ii][lr][label] + self.node_sizes[ii + lr][label] / 2
                self.draw_label(xx, yy, label, ha_dict[self.label_loc[2]])

        # Plot flows

        for lbl_l, lbl_r in self.node_pairs[ii]:
            lbot = self.node_pos_voffset[ii][0][lbl_l] + self.node_pos_bot[ii][0][lbl_l]
            rbot = self.node_pos_voffset[ii][1][lbl_r] + self.node_pos_bot[ii][1][lbl_r]
            llen = self.nodesize_l[ii][lbl_l][lbl_r]
            rlen = self.nodesize_r[ii][lbl_l][lbl_r]
            bot_lr = [lbot, rbot]
            len_lr = [llen, rlen]

            ys_d = self.create_curve(lbot, rbot)
            ys_u = self.create_curve(lbot + llen, rbot + rlen)

            # Update bottom edges at each label
            # so next strip starts at the right place
            self.node_pos_bot[ii][0][lbl_l] += llen
            self.node_pos_bot[ii][1][lbl_r] += rlen

            xx = np.linspace(x_lr[0], x_lr[1], len(ys_d))
            cc = self.combine_colours(self.color_dict[lbl_l], self.color_dict[lbl_r], len(ys_d))

            for jj in range(len(ys_d) - 1):
                self.draw_flow(
                    xx[[jj, jj + 1]],
                    ys_d[[jj, jj + 1]],
                    ys_u[[jj, jj + 1]],
                    cc[:, jj],
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
                if not (
                    val < self.value_thresh_val
                    or val < self.value_thresh_sum * self.weight_sum[ii + lr]
                    or val < self.value_thresh_max * max(self.data[2 * ii + 1])
                ):
                    self.draw_value(
                        x_lr[lr] + (1 - 2 * lr) * self.x_value_gap,
                        bot_lr[lr] + len_lr[lr] / 2,
                        val,
                        ha[lr],
                    )

        # Place "titles"
        if self.titles is not None:
            last_label = self.node_pairs[ii][-1]
            title_x = [x_lr[0] - self.x_node_width / 2, x_lr[1] + self.x_node_width / 2]

            for lr in [0, 1] if ii == 0 else [1]:
                if self.title_side in ("top", "both"):
                    if self.title_loc == "outer":
                        yt = min(self.voffset) + self.y_title_gap + self.y_frame_gap + self.plot_height
                    elif self.title_loc == "inner":
                        yt = self.y_title_gap + self.node_pos_top[ii][lr][last_label[lr]]
                    self.draw_title(title_x[lr], yt, self.titles[ii + lr], "bottom")

                if self.title_side in ("bottom", "both"):
                    if self.title_loc == "outer":
                        yt = min(self.voffset) - self.y_title_gap - self.y_frame_gap
                    elif self.title_loc == "inner":
                        yt = self.voffset[ii + lr] - self.y_title_gap
                    self.draw_title(title_x[lr], yt, self.titles[ii + lr], "top")

    ###########################################

    def draw_node(self, x, dx, y, dy, label):
        """Draw a single node"""
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

    ###########################################

    def draw_flow(self, xx, yd, yu, col):
        """Draw a single flow"""
        self.ax.fill_between(
            xx,
            yd,
            yu,
            color=col,
            alpha=self.flow_alpha,
            lw=0,
            edgecolor="none",
            snap=True,
        )
        # edges:
        if self.flow_edge:
            self.ax.plot(
                xx,
                yd,
                color=col,
                lw=self.flow_lw,
                snap=True,
            )
            self.ax.plot(
                xx,
                yu,
                color=col,
                lw=self.flow_lw,
                snap=True,
            )

    ###########################################

    def draw_label(self, x, y, label, ha):
        """Place a single label"""
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

    ###########################################

    def draw_value(self, x, y, val, ha):
        """Place a single value label"""
        self.ax.text(
            x,
            y,
            f"{format(val,self.value_format)}",
            {
                "ha": ha,
                "va": "center",
                "fontfamily": self.fontfamily,
                "fontsize": self.fontsize,
                "color": self.fontcolor,
                **self.value_font,
            },
        )

    ###########################################

    def draw_title(self, x, y, label, va):
        """Place a single title"""
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

    ###########################################

    def sort_nodes(self, lbl, node_sizes):
        """Creates a sorted list of unique labels into a list"""

        arr = {}
        for uniq in lbl.unique():
            if uniq is not None:
                arr[uniq] = True

        sort_arr = sorted(
            arr.items(),
            key=lambda item: list(node_sizes).index(item[0]),
        )

        return list(dict(sort_arr).keys())

    ###########################################

    def sort_node_sizes(self, lbl, sorting):
        """Sorts list of labels and their weights into a dictionary"""

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
            key=lambda item: s * self.sort_dict.get(item[0], item[1]),
            # sorting = 0,1,-1 affects this
        )

        sorted_labels = dict(sort_arr)

        if sorting == "center":
            # this kinda works but i dont think it's a good idea because you lose perception of relative sizes
            # probably has an off-by-one even/odd error
            sorted_labels = sorted_labels[1::2] + sorted_labels[-1::-2]

        return sorted_labels

    ###########################################

    def create_curve(self, lpoint, rpoint):
        """Create array of y values for each strip"""

        num_div = 20
        num_arr = 50

        # half at left value, half at right, convolve

        ys = np.array(num_arr * [lpoint] + num_arr * [rpoint])

        ys = np.convolve(ys, 1 / num_div * np.ones(num_div), mode="valid")

        return np.convolve(ys, 1 / num_div * np.ones(num_div), mode="valid")

    ###########################################

    def combine_colours(self, c1, c2, num_col):
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
