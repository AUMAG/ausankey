"""
Produces simple Sankey Diagrams with matplotlib.

@author: wspr

Forked from: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
"""

import matplotlib as mpl
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

    sky.plot_init()
    sky.plot_frame()

    # draw each sankey
    for ii in range(sky.num_flow):
        sky.subplot(ii)

    sky.ax.set_xticks(sky.xticks)
    # draw titles
    if sky.titles is not None:
        sky.ax.set_xticklabels(sky.titles)
        for ii in range(sky.num_flow):
            sky.plot_titles(ii)


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

    label_loc : array or str
        label_loc : strA
        label_loc : [str1, strM, strN]
        label_loc : [str1, str2,..., strN]

        Position to place labels next to the nodes. Each str can be one of:
        `"left"`, `"right"`, `"both"`, `"center"`,  `"top"`, or `"none"`.

        Three syntax variations: if just one string is provided (`strA`), use this as the option for all flows.
        If three strings provided, the first (`str1`) is the first, the third string (`strN`) is the last,
        and the second string (`strM`) is used as the option for all middle flows.

        * `str1`: position of value(s) in first flow
        * `strM`: position of value(s) in middle flows
        * `strN`: position of value(s) in last flow

        Finally, a separate string can be provided for each flow.

    label_largest: bool
        Only the label the largest valued of all nodes for each label.

    label_duplicate : bool
        When set False, will only print a middle label if that label didn't
        appear in the previous stage. This minimises chart clutter but might
        be confusing in cases, hence defaulting to True.

    label_font : dict
        Dictionary of Matplotlib text options to be passed to the labels.

    label_values : bool
        Whether to include the value of the node size with the node label text.

    label_thresh : float
        Only print labels when their node is greater or equal to this value.

    label_thresh_ofsum : float
        Only print labels when their node value is greater or equal than this percentage of the total of this stage.

    label_thresh_ofmax : float
        Only print labels when their node value is greater or equal than this percentage of the maximum total across all stages.

    other_thresh : float
        Sets threshold to recategorise nodes that are below a certain value.
        Up to three dictionary keys can be set:

        * `"val": v` — set node to other if it is less than `v`
        * `"ofsum": s` — set node to other if it is less than `s` fraction
                       of the summed total of all nodes in the current stage
        * `"ofmax": m` — set node to other if is is less than `m` fraction
                       of the maximum summed total across all stages

        If any of these criteria are met the reclassification will occur.

    other_thresh_ofsum : float
        Sets threshold to recategorise nodes that are below a certain value.
        Up to three dictionary keys can be set:

        * `"val": v` — set node to other if it is less than `v`
        * `"ofsum": s` — set node to other if it is less than `s` fraction
                       of the summed total of all nodes in the current stage
        * `"ofmax": m` — set node to other if is is less than `m` fraction
                       of the maximum summed total across all stages

        If any of these criteria are met the reclassification will occur.

    other_thresh_ofmax : float
        Sets threshold to recategorise nodes that are below a certain value.
        Up to three dictionary keys can be set:

        * `"val": v` — set node to other if it is less than `v`
        * `"ofsum": s` — set node to other if it is less than `s` fraction
                       of the summed total of all nodes in the current stage
        * `"ofmax": m` — set node to other if is is less than `m` fraction
                       of the maximum summed total across all stages

        If any of these criteria are met the reclassification will occur.

    other_name : str
        The string used to rename nodes to if they are classified as “other”.

    percent_loc : array or str
        percent_loc : strA
        percent_loc : [str1, strM, strN]
        percent_loc : [str1, str2,..., strN]

        Position to place percentage labels next to the nodes. Each str can be one of:
        `"left"`, `"right"`, `"center"`, or `"none"`.

        Three syntax variations: if just one string is provided (`strA`), use this as the option for all nodes.
        If three strings provided, the first (`str1`) is the first, the third string (`strN`) is the last,
        and the second string (`strM`) is used as the option for all middle ones.

        * `str1`: position of value(s) in first
        * `strM`: position of value(s) in middle
        * `strN`: position of value(s) in last

        Finally, a separate string can be provided for each node.

    percent_loc_ht : array or float
        percent_loc_ht : numA
        percent_loc_ht : [num1, numM, numN]
        percent_loc_ht : [num1, num2,..., numN]

        Vertical position to place percentage value, a normalised position between 0 and 1 relative to the bottom and top of the node. Default = 0.5.

    percent_thresh : float
        Only print percentage labels greater or equal to this value. In normalised units where 1 = 100%.

    percent_thresh : float
        Only print percentage labels if the value of the node is greater or equal to this value.

    percent_format : str
        String formatting specification passed internally to the `format()` function.

    percent_font : dict
        Dictionary of Matplotlib text options to be passed to the percentage labels.

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

    value_loc : array or str
        value_loc : strA
        value_loc : [str1, strM, strN]
        value_loc : [str1, str2,..., strN]

        Position to place values next to the nodes corresponding to the sizes.
        These are placed within the flows at the beginning (left) and end (right) of each one.
        Each str can be one of: `"left"`, `"right"`, `"both"`, or `"none"`

        Three syntax variations: if just one string is provided (`strA`), use this as the option for all flows.
        If three strings provided, the first (`str1`) is the first, the third string (`strN`) is the last,
        and the second string (`strM`) is used as the option for all middle flows.

        * `str1`: position of value(s) in first flow
        * `strM`: position of value(s) in middle flows
        * `strN`: position of value(s) in last flow

        Finally, a separate string can be provided for each flow.

    value_format : str
        String formatting specification passed internally to the `format()` function.

    value_fn : lambda function
        Alternative to value_format. Transform the value label using the specified lambda function; the output must be a string. E.g.:

            value_fn = lambda x: f"${round(x)}"

    value_gap : float
        Horizontal space fraction between the edge of the node and the value label.
        Defaults to `label_gap`.

    value_font : dict
        Dictionary of Matplotlib text options to be passed to the value labels.

    value_thresh : float
        Only print labels larger than this absolute value threshold.

    value_thresh_ofsum : float
        Only print labels larger than this threshold as a fraction of the sum of all node weights in the stage.

    value_thresh_ofmax : float
        Only print labels larger than this threshold as a fraction of the maximum of the summed weights across all stages.

    value_duplicate: bool
        When `True` (default), all values are printed. When `False`, only print a right value if it is not equal to the preceding left value.
    """

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
        label_largest=None,
        label_values=None,
        label_thresh=0,
        label_thresh_ofsum=0,
        label_thresh_ofmax=0,
        node_lw=1,
        node_width=0.02,
        node_gap=0.05,
        node_alpha=1,
        node_edge=None,
        other_thresh=0,
        other_thresh_ofmax=0,
        other_thresh_ofsum=0,
        other_name="Other",
        percent_loc="none",
        percent_loc_ht=0.5,
        percent_thresh=0,
        percent_thresh_val=0,
        percent_thresh_ofmax=0,
        percent_format="2.0f",
        percent_font=None,
        sort="bottom",  # "top", "bottom", "none"
        sort_dict=None,
        titles=None,
        title_gap=0.05,
        title_side="top",  # "bottom", "both"
        title_loc="inner",  # "outer"
        title_font=None,
        valign="bottom",  # "top","center"
        value_format=".0f",
        value_fn=None,
        value_gap=None,
        value_font=None,
        value_loc=("both", "right", "right"),
        value_thresh=0,
        value_thresh_ofsum=0,
        value_thresh_ofmax=0,
        value_duplicate=None,
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
        self.frame_color = frame_color or [0, 0, 0, 1]
        self.frame_lw = frame_lw
        self.label_dict = label_dict or {}
        self.label_width = label_width
        self.label_gap = label_gap
        self.label_loc = label_loc
        self.label_font = label_font or {}
        self.label_thresh = label_thresh
        self.label_thresh_ofsum = label_thresh_ofsum
        self.label_thresh_ofmax = label_thresh_ofmax
        self.label_duplicate = True if label_duplicate is None else label_duplicate
        self.label_largest = False if label_largest is None else label_largest
        self.label_values = False if label_values is None else label_values
        self.node_lw = node_lw
        self.node_width = node_width
        self.node_gap = node_gap
        self.node_alpha = node_alpha
        self.node_edge = node_edge or False
        self.other_name = other_name
        self.other_thresh = other_thresh
        self.other_thresh_ofmax = other_thresh_ofmax
        self.other_thresh_ofsum = other_thresh_ofsum
        self.percent_loc = percent_loc
        self.percent_loc_ht = percent_loc_ht
        self.percent_thresh = percent_thresh
        self.percent_thresh_val = percent_thresh_val
        self.percent_thresh_ofmax = percent_thresh_ofmax
        self.percent_format = percent_format
        self.percent_font = percent_font
        self.sort = sort
        self.sort_dict = sort_dict or {}
        self.titles = titles
        self.title_font = title_font or {"fontweight": "bold"}
        self.title_gap = title_gap
        self.title_loc = title_loc
        self.title_side = title_side
        self.valign = valign
        self.value_format = value_format
        self.value_fn = value_fn
        self.value_gap = label_gap if value_gap is None else value_gap
        self.value_font = value_font or {}
        self.value_loc = value_loc
        self.value_thresh = value_thresh
        self.value_thresh_ofsum = value_thresh_ofsum
        self.value_thresh_ofmax = value_thresh_ofmax
        self.value_duplicate = True if value_duplicate is None else value_duplicate

    ###########################################

    def setup(self, data):
        """Calculates all parameters needed to plot the graph"""

        self.data = data.fillna(np.nan).replace([np.nan], [None])
        # replaces NaN etc with None

        num_col = len(self.data.columns)
        self.data.columns = range(num_col)  # force numeric column headings
        self.num_stages = int(num_col / 2)  # number of stages
        self.num_flow = self.num_stages - 1

        short_num = 3

        # arg syntactic sugar
        def fix_length(str_or_array, nmax):
            if isinstance(str_or_array, (float, str)):
                return np.repeat(str_or_array, nmax)
            if len(str_or_array) == short_num and nmax == short_num - 1:
                return np.concatenate([[str_or_array[0]], [str_or_array[2]]])
            if len(str_or_array) == short_num and nmax > short_num:
                return np.concatenate([[str_or_array[0]], np.repeat(str_or_array[1], nmax - 2), [str_or_array[2]]])
            return str_or_array

        self.value_loc = fix_length(self.value_loc, self.num_flow)
        self.label_loc = fix_length(self.label_loc, self.num_stages)
        self.percent_loc = fix_length(self.percent_loc, self.num_stages)
        self.percent_loc_ht = fix_length(self.percent_loc_ht, self.num_stages)

        # sizes
        self.node_sizes = {}
        self.nodes_uniq = {}

        self.node_pos_voffset = {}
        self.node_pos_bot = {}
        self.node_pos_top = {}

        # weight and reclassify
        self.weight_labels()
        for ii in range(self.num_stages):
            for nn, lbl in enumerate([x for x in self.data[2 * ii] if x is not None]):
                val = self.node_sizes[ii][lbl]
                if (
                    val < self.other_thresh
                    or val < self.other_thresh_ofsum * self.weight_sum[ii]
                    or val < self.other_thresh_ofmax * self.plot_height_nom
                ):
                    self.data.iat[nn, 2 * ii] = self.other_name
        self.weight_labels()

        # sort and calc
        for ii in range(self.num_stages):
            self.node_sizes[ii] = self.sort_node_sizes(self.node_sizes[ii], self.sort)

        self.calc_plot_height()
        self.calc_plot_dimens()

        self.x_lr = {}
        self.nodesize_l = {}
        self.nodesize_r = {}
        self.node_pairs = {}
        self.xticks = np.empty(self.num_stages)
        for ii in range(self.num_flow):
            x_left = (
                self.x_node_width + self.x_label_gap + self.x_label_width + ii * (self.sub_width + self.x_node_width)
            )
            if ii == 0:
                self.xticks[ii] = self.x_label_gap + self.x_node_width / 2
            self.xticks[ii + 1] = x_left + self.sub_width + self.x_node_width / 2
            self.x_lr[ii] = (x_left, x_left + self.sub_width)
            self.nodesize_l[ii] = {}
            self.nodesize_r[ii] = {}
            self.node_pairs[ii] = []
            for lbl_l in self.node_sizes[ii]:
                self.nodesize_l[ii][lbl_l] = {}
                self.nodesize_r[ii][lbl_l] = {}
                for lbl_r in self.node_sizes[ii + 1]:
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
            prev_label = None  # avoid lint error
            for lr in [0, 1]:
                for i, (label, node_height) in enumerate(self.node_sizes[ii + lr].items()):
                    this_side_height = self.node_indiv_heights[ii][lr].get(label, 0)
                    self.node_pos_voffset[ii][lr][label] = self.vscale * (node_height - this_side_height)
                    if i == 0:
                        tmp_top = self.voffset[ii + lr]
                    else:
                        tmp_top = self.node_pos_top[ii][lr][prev_label] + self.y_node_gap
                    self.node_pos_bot[ii][lr][label] = tmp_top
                    self.node_pos_top[ii][lr][label] = tmp_top + node_height
                    prev_label = label

        # labels
        label_record = self.data[range(0, 2 * self.num_stages, 2)].to_records(index=False)
        flattened = [item for sublist in label_record for item in sublist]
        self.all_labels = pd.Series(flattened).unique()

        # If no color_dict given, make one
        color_dict_new = {}
        cmap = getattr(mpl.cm, self.colormap, None)
        color_palette = cmap(np.linspace(0, 1, len(self.all_labels)))
        for i, label in enumerate(self.all_labels):
            color_dict_new[label] = self.color_dict.get(label, color_palette[i])
        self.color_dict = color_dict_new

    ###########################################

    def plot_init(self):
        # initialise plot
        self.ax = self.ax or plt.gca()
        self.ax.axis("off")

    ###########################################

    def weight_labels(self):
        """Calculates sizes of each node, taking into account discontinuities"""
        self.weight_sum = np.empty(self.num_stages)

        self.node_indiv_heights = {}
        self.nodes_largest = {}

        for ii in range(self.num_stages):
            self.nodes_uniq[ii] = pd.Series(self.data[2 * ii]).dropna().unique()

        for ii in range(self.num_stages):
            self.node_sizes[ii] = {}
            self.node_indiv_heights[ii] = {}
            self.node_indiv_heights[ii][0] = {}
            if ii > 0:
                self.node_indiv_heights[ii - 1][1] = {}
            for lbl in self.nodes_uniq[ii]:
                i_p = 2 if ii > 0 else 0
                i_n = 2 if ii < self.num_flow else 0
                ind_this = self.data[2 * ii] == lbl
                none_prev = self.data[2 * ii - i_p].isna()
                none_next = self.data[2 * ii + i_n].isna()

                ind_cont = ind_this & ~none_prev & ~none_next
                ind_only = ind_this & none_prev & none_next
                ind_stop = ind_this & ~none_prev & none_next
                ind_strt = ind_this & none_prev & ~none_next

                weight_cont = self.data[2 * ii + 1][ind_cont].sum()
                weight_only = self.data[2 * ii + 1][ind_only].sum()
                weight_stop = self.data[2 * ii + 1][ind_stop].sum()
                weight_strt = self.data[2 * ii + 1][ind_strt].sum()

                if ii == 0:
                    self.node_indiv_heights[ii][0][lbl] = weight_cont + weight_only + weight_stop
                elif ii == self.num_stages:
                    self.node_indiv_heights[ii - 1][1][lbl] = weight_cont + weight_only + weight_strt
                else:
                    self.node_indiv_heights[ii][0][lbl] = weight_cont + weight_only + weight_stop
                    self.node_indiv_heights[ii - 1][1][lbl] = weight_cont + weight_only + weight_strt
                self.node_sizes[ii][lbl] = weight_cont + weight_only + max(weight_stop, weight_strt)
                self.nodes_largest[lbl] = self.node_sizes[ii][lbl] if self.node_sizes[ii][lbl] > self.nodes_largest.get(lbl,0) else self.nodes_largest.get(lbl,0)

            self.weight_sum[ii] = pd.Series(self.node_sizes[ii].values()).sum()

        self.plot_height_nom = max(self.weight_sum)

    ###########################################

    def calc_plot_height(self):
        """Calculate column heights, offsets, and total plot height"""

        vscale_dict = {"top": 1, "center": 0.5, "bottom": 0}
        self.vscale = vscale_dict.get(self.valign, 0)

        self.voffset = np.empty(self.num_stages)
        col_hgt = np.empty(self.num_stages)
        for ii in range(self.num_stages):
            col_hgt[ii] = self.weight_sum[ii] + (len(self.nodes_uniq[ii]) - 1) * self.node_gap * self.plot_height_nom
            self.voffset[ii] = self.vscale * (col_hgt[0] - col_hgt[ii])

        self.plot_height = max(col_hgt)

    ###########################################

    def calc_plot_dimens(self):
        """Calculate absolute size of plot dimens based on scaling factors"""

        # overall dimensions
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
        self.y_label_gap = self.label_gap * self.plot_height_nom

        # horizontal positions
        self.x_node_width = self.node_width * self.plot_width_nom
        self.x_label_width = self.label_width * self.plot_width_nom
        self.x_label_gap = self.label_gap * self.plot_width_nom
        self.x_value_gap = self.value_gap * self.plot_width_nom

    ###########################################

    def plot_frame(self):
        """Plot frame on top/bottom edges.

        We always plot them to ensure the exported plot width is correct.
        If the frame is not requested it is drawn with 100% transparency.
        """

        frame_top = self.frame_side in ("top", "both")
        frame_bot = self.frame_side in ("bottom", "both")

        self.ax.plot(
            [0, self.plot_width],
            min(self.voffset) + (self.plot_height) + self.y_frame_gap + [0, 0],
            color=self.frame_color if frame_top else [1, 1, 1, 0],
            lw=self.frame_lw,
        )

        self.ax.plot(
            [0, self.plot_width],
            min(self.voffset) - self.y_frame_gap + [0, 0],
            color=self.frame_color if frame_bot else [1, 1, 1, 0],
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
            for label in self.node_sizes[ii + lr]:
                self.draw_node(
                    x_lr[lr] - self.x_node_width * (1 - lr),
                    self.x_node_width,
                    self.node_pos_bot[ii][lr][label],
                    self.node_sizes[ii + lr][label],
                    label,
                )

        # Draw node labels

        for lr in [0, 1] if ii == 0 else [1]:
            label_bool = ii + lr == 0 or ii + lr == self.num_flow or self.label_duplicate
            loc = self.label_loc[ii + lr]
            if not label_bool:
                continue

            for label in self.node_sizes[ii + lr]:
                val = self.node_sizes[ii + lr][label]
                if (val is None) or (val == 0):
                    continue

                check_not_largest = self.label_largest and (
                    val < self.nodes_largest[label]
                )
                check_less_thresh = (
                    val < self.label_thresh
                    or val < self.label_thresh_ofsum * self.weight_sum[ii + lr]
                    or val < self.label_thresh_ofmax * self.plot_height_nom
                )
                if check_less_thresh or check_not_largest:
                    continue

                if loc in ("left", "both"):
                    xx = x_lr[lr] - self.x_label_gap + (lr - 1) * self.x_node_width

                    if label_bool or label not in self.node_sizes[ii]:
                        yy = self.node_pos_bot[ii][lr][label] + val / 2
                        self.draw_label(xx, yy, label, "right", val)

                if loc in ("center"):
                    xx = x_lr[lr] + (2 * lr - 1) * self.x_node_width / 2

                    if label_bool or label not in self.node_sizes[ii]:
                        yy = self.node_pos_bot[ii][lr][label] + val / 2
                        self.draw_label(xx, yy, label, "center", val)

                if loc in ("top"):
                    xx = x_lr[lr] + (2 * lr - 1) * self.x_node_width / 2

                    if label_bool or label not in self.node_sizes[ii]:
                        yy = self.node_pos_bot[ii][lr][label] + val + self.y_label_gap
                        self.draw_label(xx, yy, label, "center", val)

                if loc in ("right", "both"):
                    xx = x_lr[lr] + self.x_label_gap + lr * self.x_node_width

                    if label_bool or label not in self.node_sizes[ii]:
                        yy = self.node_pos_bot[ii][lr][label] + val / 2
                        self.draw_label(xx, yy, label, "left", val)

        # percent labels

        for lr in [0, 1] if ii == 0 else [1]:
            loc = self.percent_loc[ii + lr]
            ht = self.percent_loc_ht[ii + lr]

            for label in self.node_sizes[ii + lr]:
                absval = self.node_sizes[ii + lr][label]
                val = 100 * self.node_sizes[ii + lr][label] / self.weight_sum[ii + lr]
                valstr = f"{format(val,self.percent_format)}%"
                if (
                    (val < 100 * self.percent_thresh)
                    or (absval < self.percent_thresh_val)
                    or (absval < self.percent_thresh_ofmax * self.plot_height_nom)
                ):
                    continue

                yy = self.node_pos_bot[ii][lr][label] + ht * self.node_sizes[ii + lr][label]

                if loc in ("left"):
                    xx = x_lr[lr] - self.x_label_gap + (lr - 1) * self.x_node_width
                    self.draw_percent(xx, yy, valstr, "right", font=self.percent_font)

                if loc in ("center"):
                    xx = x_lr[lr] + (2 * lr - 1) * self.x_node_width / 2
                    self.draw_percent(xx, yy, valstr, "center", font=self.percent_font)

                if loc in ("right"):
                    xx = x_lr[lr] + self.x_label_gap + lr * self.x_node_width
                    self.draw_percent(xx, yy, valstr, "left", font=self.percent_font)

        # Plot flows

        for lbl_l, lbl_r in self.node_pairs[ii]:
            lbot = self.node_pos_voffset[ii][0][lbl_l] + self.node_pos_bot[ii][0][lbl_l]
            rbot = self.node_pos_voffset[ii][1][lbl_r] + self.node_pos_bot[ii][1][lbl_r]
            llen = self.nodesize_l[ii][lbl_l][lbl_r]
            rlen = self.nodesize_r[ii][lbl_l][lbl_r]
            lbl_lr = [lbl_l, lbl_r]
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

            sides = []
            if self.value_loc[ii] in ("left", "both"):
                sides.append(0)
            if self.value_loc[ii] in ("right", "both"):
                sides.append(1)
            for lr in sides:
                val = len_lr[lr]
                if (
                    val < self.value_thresh
                    or val < self.value_thresh_ofsum * self.weight_sum[ii + lr]
                    or val < self.value_thresh_ofmax * self.plot_height_nom
                ):
                    continue  # dont plot flow label if less than threshold(s)
                if self.label_values and self.node_sizes[ii + lr][lbl_lr[lr]] == len_lr[lr]:
                    continue  # dont plot flow label if equal the adjacent node label
                if not (self.value_duplicate) and lr == 1 and len_lr[0] == len_lr[1]:
                    continue  # don't plot right flow label is equal to left flow label
                if self.label_values and lr == 0 and len_lr[0] == self.node_sizes[ii + 1][lbl_r]:
                    continue  # don't plot left value if it is same as succeeding flow value

                self.draw_value(
                    x_lr[lr] + (1 - 2 * lr) * self.x_value_gap,
                    bot_lr[lr] + len_lr[lr] / 2,
                    val,
                    ("left", "right")[lr],
                )

    ###########################################

    def plot_titles(self, ii):
        """Subroutine for placing titles"""

        x_lr = self.x_lr[ii]

        title_x = [x_lr[0] - self.x_node_width / 2, x_lr[1] + self.x_node_width / 2]

        for lr in [0, 1] if ii == 0 else [1]:
            last_label = list(self.node_sizes[ii + lr])[-1]
            if self.title_side in ("top", "both"):
                if self.title_loc == "outer":
                    yt = min(self.voffset) + self.y_title_gap + self.y_frame_gap + self.plot_height
                elif self.title_loc == "inner":
                    yt = self.y_title_gap + self.node_pos_top[ii][lr][last_label]
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

    def draw_label(self, x, y, label, ha, val=None, font=None):
        """Place a single label"""

        valstr = ""
        font = font or self.label_font
        if self.label_values and val is not None:
            value_fn = self.value_fn or (lambda val: f"\n{format(val,self.value_format)}")
            valstr = value_fn(val)

        self.ax.text(
            x,
            y,
            self.label_dict.get(label, label) + valstr,
            {
                "ha": ha,
                "va": "center",
                "fontfamily": self.fontfamily,
                "fontsize": self.fontsize,
                "color": self.fontcolor,
                **font,
            },
        )

    ###########################################

    def draw_percent(self, x, y, label, ha, font=None):
        """Place a single label"""

        font = font or self.label_font
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
                **font,
            },
        )

    ###########################################

    def draw_value(self, x, y, val, ha, format_=None, font=None):
        """Place a single value label"""

        format_ = format_ or self.value_format
        font = font or self.value_font
        self.ax.text(
            x,
            y,
            f"{format(val,format_)}",
            {
                "ha": ha,
                "va": "center",
                "fontfamily": self.fontfamily,
                "fontsize": self.fontsize,
                "color": self.fontcolor,
                **font,
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
