"""
Produces simple Sankey Diagrams with matplotlib.

@author: wspr

Forked from: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class SankeyError(Exception):
    pass


def sankey(
    data,
    aspect=4,
    alpha=0.65,
    ax=None,
    node_width=0.02,
    node_gap=0.05,
    color_dict=None,
    colormap="viridis",
    flow_edge=None,
    fontcolor="black",
    fontfamily="sans-serif",
    fontsize=12,
    frame_side="none",
    frame_gap=0.1,
    frame_color=None,
    label_dict=None,
    label_width=0,
    label_gap=0.01,
    label_loc=None,
    label_fontcolor=None,
    label_fontfamily=None,
    label_fontsize=None,
    label_fontstyle="normal",
    label_fontweight="normal",
    titles=None,
    title_gap=0.05,
    title_side="top",  # "bottom", "both"
    title_loc="inner",  # "outer"
    title_fontcolor=None,
    title_fontfamily=None,
    title_fontsize=None,
    title_fontstyle="normal",
    title_fontweight="bold",
    sort="bottom",  # "top", "bottom", "none"
    valign="bottom",  # "top","center"
):
    """Make Sankey Diagram with left-right flow

    Parameters
    ----------
    data : DataFrame
        pandas dataframe of labels and weights in alternating columns

    alpha : float
        Opacity of the flows (`0.0` = transparent, `1.0` = opaque)

    aspect : float
        vertical extent of the diagram in units of horizontal extent

    ax : Axis
        Matplotlib plot axis to use

    node_width : float
        Normalised horizontal width of the data bars
        (1.0 = 100% of plot width)

    node_gap : float
        Normalised vertical gap between successive data bars
        (1.0 = 100% of nominal plot height).

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
        (1.0 = 100% of plot height)

    label_gap : float
        Normalised horizontal gap between the left/right of the
        plot edges and the label
        (1.0 = 100% of plot width)

    label_loc : [str1, str2, str3]
        Position to place labels next to the nodes.
        * `str1`: position of first labels (`"left"`, `"right"`, or `"none"`)
        * `str2`: position of middle labels (`"left"`, `"right"`, `"both"`, or `"none"`)
        * `str3`: position of last labels (`"left"`, `"right"`, or `"none"`)

    label_fontfamily: str
        Font family of the node labels.
        If not set inherits from option `fontfamily`.
        Passed through to Matplotlib's text option `fontfamily`.

    label_fontweight: str
        Font weight of the node labels.
        Passed through to Matplotlib's text option `fontweight`.

    label_fontstyle: str
        Font style of the node labels.
        Passed through to Matplotlib's text option `fontstyle`.

    label_fontsize: float
        Font size of the node labels.
        If not set inherits from option `fontsize`.
        Passed through to Matplotlib's text option `fontsize`.

    label_fontcolor: color
        Font colour of the node labels.
        If not set inherits from option `fontcolor`.
        Passed through to Matplotlib's text option `color`.

    sort : int
        Sorting routine to use for the data.
        * `"top"`: data is sorted with largest entries on top
        * `"bottom"`: data is sorted with largest entries on bottom
        * `"none"`: data is presented in the same order as it appears in the DataFrame

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

    title_fontfamily: str
        Font family of the titles.
        If not set inherits from option `fontfamily`.
        Passed through to Matplotlib's text option `fontfamily`.

    title_fontweight: str
        Font weight of the titles.
        Passed through to Matplotlib's text option `fontweight`.

    title_fontstyle: str
        Font style of the titles.
        Passed through to Matplotlib's text option `fontstyle`.

    title_fontsize: float
        Font size of the titles.
        If not set inherits from option `fontsize`.
        Passed through to Matplotlib's text option `fontsize`.

    title_fontcolor: color
        Font colour of the titles.
        If not set inherits from option `fontcolor`.
        Passed through to Matplotlib's text option `color`.

    valign : str
        Vertical alignment of the data bars at each stage,
        with respect to the whole plot.
        Allowed values: `"top"`, `"bottom"`, or `"center"`


    Returns
    -------

    None
    """

    num_col = len(data.columns)
    data.columns = range(num_col)  # force numeric column headings
    num_side = int(num_col / 2)  # number of labels
    num_flow = num_side - 1

    # sizes
    weight_sum = np.empty(num_side)
    num_uniq = np.empty(num_side)
    col_hgt = np.empty(num_side)
    node_sizes = {}
    nodes_uniq = {}
    for ii in range(num_side):
        nodes_uniq[ii] = pd.Series(data[2 * ii]).unique()
        num_uniq[ii] = len(nodes_uniq[ii])

    for ii in range(num_side):
        node_sizes[ii] = {}
        for lbl in nodes_uniq[ii]:
            if ii == 0:
                ind_prev = data[2 * ii + 0] == lbl
                ind_this = data[2 * ii + 0] == lbl
                ind_next = data[2 * ii + 2] == lbl
            elif ii == num_flow:
                ind_prev = data[2 * ii - 2] == lbl
                ind_this = data[2 * ii + 0] == lbl
                ind_next = data[2 * ii + 0] == lbl
            else:
                ind_prev = data[2 * ii - 2] == lbl
                ind_this = data[2 * ii + 0] == lbl
                ind_next = data[2 * ii + 2] == lbl
            weight_cont = data[2 * ii + 1][ind_this & ind_prev & ind_next].sum()
            weight_only = data[2 * ii + 1][ind_this & ~ind_prev & ~ind_next].sum()
            weight_stop = data[2 * ii + 1][ind_this & ind_prev & ~ind_next].sum()
            weight_strt = data[2 * ii + 1][ind_this & ~ind_prev & ind_next].sum()
            node_sizes[ii][lbl] = weight_cont + weight_only + max(weight_stop, weight_strt)
        node_sizes[ii] = sort_dict(node_sizes[ii], sort)
        weight_sum[ii] = pd.Series(node_sizes[ii].values()).sum()

    for ii in range(num_side):
        col_hgt[ii] = weight_sum[ii] + (num_uniq[ii] - 1) * node_gap * max(weight_sum)

    # overall dimensions
    plot_height = max(col_hgt)
    sub_width = plot_height / aspect
    plot_width = (
        (num_side - 1) * sub_width + 2 * sub_width * (label_gap + label_width) + num_side * sub_width * node_width
    )

    # offsets for alignment
    voffset = np.empty(num_side)
    if valign == "top":
        vscale = 1
    elif valign == "center":
        vscale = 0.5
    else:  # bottom, or undefined
        vscale = 0

    for ii in range(num_side):
        voffset[ii] = vscale * (col_hgt[1] - col_hgt[ii])

    # labels
    label_record = data[range(0, 2 * num_side, 2)].to_records(index=False)
    flattened = [item for sublist in label_record for item in sublist]
    flatcat = pd.Series(flattened).unique()

    # If no color_dict given, make one
    color_dict = color_dict or {}
    color_dict_new = {}
    cmap = plt.cm.get_cmap(colormap)
    color_palette = cmap(np.linspace(0, 1, len(flatcat)))
    for i, label in enumerate(flatcat):
        color_dict_new[label] = color_dict.get(label, color_palette[i])

    # initialise plot
    ax = ax or plt.gca()

    # frame on top/bottom edge
    frame_top = frame_side in ("top", "both")
    frame_bot = frame_side in ("bottom", "both")

    frame_color = frame_color or [0, 0, 0, 1]

    y_frame_gap = frame_gap * plot_height

    col = frame_color if frame_top else [1, 1, 1, 0]
    ax.plot(
        [0, plot_width],
        min(voffset) + (plot_height) + y_frame_gap + [0, 0],
        color=col,
    )

    col = frame_color if frame_bot else [1, 1, 1, 0]
    ax.plot(
        [0, plot_width],
        min(voffset) - y_frame_gap + [0, 0],
        color=col,
    )

    # draw each segment
    for ii in range(num_flow):
        _sankey(
            ii,
            num_flow,
            data,
            node_sizes=node_sizes,
            titles=titles,
            title_gap=title_gap,
            title_side=title_side,
            title_loc=title_loc,
            title_fontweight=title_fontweight,
            title_fontsize=title_fontsize or fontsize or 14,
            title_fontcolor=title_fontcolor or fontcolor or "black",
            title_fontfamily=title_fontfamily or fontfamily or "sans-serif",
            title_fontstyle=title_fontstyle,
            color_dict=color_dict_new,
            flow_edge=flow_edge or False,
            frame_gap=frame_gap,
            label_dict=label_dict or {},
            label_width=label_width,
            label_gap=label_gap,
            label_loc=label_loc or ["left", "none", "right"],
            label_fontsize=label_fontsize or fontsize or 12,
            label_fontweight=label_fontweight,
            label_fontcolor=label_fontcolor or fontcolor or "black",
            label_fontfamily=label_fontfamily or fontfamily or "sans-serif",
            label_fontstyle=label_fontstyle,
            node_width=node_width,
            node_gap=node_gap,
            sub_width=sub_width,
            plot_height=plot_height,
            alpha=alpha,
            voffset=voffset,
            valign=valign,
            ax=ax,
        )

    # complete plot
    ax.axis("off")


###########################################


def _sankey(
    ii,
    num_flow,
    data,
    color_dict=None,
    flow_edge=None,
    frame_gap=None,
    node_sizes=None,
    titles=None,
    title_gap=None,
    title_side=None,
    title_loc=None,
    title_fontweight=None,
    title_fontsize=None,
    title_fontcolor=None,
    title_fontfamily=None,
    title_fontstyle=None,
    plot_height=None,
    sub_width=None,
    label_dict=None,
    label_width=None,
    label_gap=None,
    label_loc=None,
    label_fontsize=None,
    label_fontweight=None,
    label_fontcolor=None,
    label_fontfamily=None,
    label_fontstyle=None,
    node_width=None,
    node_gap=None,
    alpha=None,
    voffset=None,
    valign=None,
    ax=None,
):
    """Subroutine for plotting horizontal sections of the Sankey plot

    Some special-casing is used for plotting/labelling differently
    for the first and last cases.
    """

    if flow_edge:
        edge_alpha = 1
        edge_lw = 1
    else:
        edge_alpha = alpha
        edge_lw = 0

    labelind = 2 * ii
    weightind = 2 * ii + 1

    if ii < num_flow - 1:
        labels_lr = [
            pd.Series(data[labelind]),
            pd.Series(data[labelind + 2]),
            pd.Series(data[labelind + 4]),
        ]
        weights_lr = [
            pd.Series(data[weightind]),
            pd.Series(data[weightind + 2]),
            pd.Series(data[weightind + 4]),
        ]
    else:
        labels_lr = [
            pd.Series(data[labelind]),
            pd.Series(data[labelind + 2]),
            pd.Series(data[labelind + 2]),
        ]
        weights_lr = [
            pd.Series(data[weightind]),
            pd.Series(data[weightind + 2]),
            pd.Series(data[weightind + 2]),
        ]

    nodes_lr = [
        sort_nodes(labels_lr[0], node_sizes[ii]),
        sort_nodes(labels_lr[1], node_sizes[ii + 1]),
    ]

    # check colours
    check_colors_match_labels(labels_lr, color_dict)

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
    y_node_gap = node_gap * plot_height

    if valign == "top":
        vscale = 1
    elif valign == "center":
        vscale = 0.5
    else:  # bottom, or undefined
        vscale = 0

    node_voffset = [{}, {}]
    node_pos_bot = [{}, {}]
    node_pos_top = [{}, {}]

    for lr in [0, 1]:
        for i, label in enumerate(nodes_lr[lr]):
            node_height = node_sizes[ii + lr][label]
            this_side_height = weights_lr[lr][labels_lr[lr] == label].sum()
            node_voffset[lr][label] = vscale * (node_height - this_side_height)
            next_bot = node_pos_top[lr][nodes_lr[lr][i - 1]] + y_node_gap if i > 0 else 0
            node_pos_bot[lr][label] = voffset[ii + lr] if i == 0 else next_bot
            node_pos_top[lr][label] = node_pos_bot[lr][label] + node_height

    # horizontal positions of nodes
    x_node_width = node_width * sub_width
    x_label_width = label_width * sub_width
    x_label_gap = label_gap * sub_width
    x_left = x_node_width + x_label_gap + x_label_width + ii * (sub_width + x_node_width)
    x_right = x_left + sub_width

    # Draw nodes and their labels

    def draw_node(x, dx, y, dy, label):
        ax.fill_between(
            [x, x + dx],
            y,
            y + dy,
            color=color_dict[label],
            alpha=1,
            lw=edge_lw,
            snap=True,
        )

    def draw_label(x, y, label, ha, va):
        ax.text(
            x,
            y,
            label_dict.get(label, label),
            {"ha": ha, "va": va},
            fontweight=label_fontweight,
            fontstyle=label_fontstyle,
            fontfamily=label_fontfamily,
            fontsize=label_fontsize,
            color=label_fontcolor,
        )

    for label in nodes_lr[0]:
        lbot = node_pos_bot[0][label]
        lll = node_sizes[ii][label]

        if ii == 0 and label_loc[0] != "none":  # first label
            if label_loc[0] in ("left"):
                xx = x_left - x_label_gap - x_node_width
                ha = "right"
            elif label_loc[0] in ("right"):
                xx = x_left + x_label_gap
                ha = "left"
            draw_label(
                xx,
                lbot + lll / 2,
                label,
                ha,
                "center",
            )
        elif ii > 0 and label_loc[1] in ("left", "both"):  # inside labels
            draw_label(
                x_left + x_label_gap,
                lbot + lll / 2,
                label,
                "left",
                "center",
            )
        wd = 2 if ii == 0 else 1
        draw_node(x_left - wd * x_node_width / 2, wd * x_node_width / 2, lbot, lll, label)

    for label in nodes_lr[1]:
        rbot = node_pos_bot[1][label]
        rrr = node_sizes[ii + 1][label]

        if ii < num_flow - 1 and label_loc[1] in ("right", "both"):  # inside labels
            draw_label(
                x_right - x_label_gap,
                rbot + rrr / 2,
                label,
                "right",
                "center",
            )
        if ii == num_flow - 1 and label_loc[2] != "none":  # last time
            if label_loc[2] in ("left"):
                xx = x_right - x_label_gap
                ha = "right"
            elif label_loc[2] in ("right"):
                xx = x_right + x_label_gap + x_node_width
                ha = "left"
            draw_label(
                xx,
                rbot + rrr / 2,
                label,
                ha,
                "center",
            )

        wd = 2 if ii == num_flow - 1 else 1
        draw_node(x_right, wd * x_node_width / 2, rbot, rrr, label)

    # Plot flows
    for lbl_l in nodes_lr[0]:
        for lbl_r in nodes_lr[1]:
            lind = labels_lr[0] == lbl_l
            rind = labels_lr[1] == lbl_r
            if not any(lind & rind):
                continue

            lbot = node_voffset[0][lbl_l] + node_pos_bot[0][lbl_l]
            rbot = node_voffset[1][lbl_r] + node_pos_bot[1][lbl_r]
            lnode = nodesize[0][lbl_l][lbl_r]
            rnode = nodesize[1][lbl_l][lbl_r]

            ys_d = create_curve(lbot, rbot)
            ys_u = create_curve(lbot + lnode, rbot + rnode)

            # Update bottom edges at each label
            # so next strip starts at the right place
            node_pos_bot[0][lbl_l] += lnode
            node_pos_bot[1][lbl_r] += rnode

            xx = np.linspace(x_left, x_right, len(ys_d))
            cc = combine_colours(color_dict[lbl_l], color_dict[lbl_r], len(ys_d))

            for jj in range(len(ys_d) - 1):
                ax.fill_between(
                    xx[[jj, jj + 1]],
                    ys_d[[jj, jj + 1]],
                    ys_u[[jj, jj + 1]],
                    color=cc[:, jj],
                    alpha=alpha,
                    lw=0,
                    edgecolor="none",
                    snap=True,
                )
                ax.plot(
                    xx[[jj, jj + 1]],
                    ys_d[[jj, jj + 1]],
                    color=cc[:, jj],
                    alpha=edge_alpha,
                    lw=edge_lw,
                    snap=True,
                )
                ax.plot(
                    xx[[jj, jj + 1]],
                    ys_u[[jj, jj + 1]],
                    color=cc[:, jj],
                    alpha=edge_alpha,
                    lw=edge_lw,
                    snap=True,
                )

    # Place "titles"
    if titles is not None:
        last_label = [lbl_l, lbl_r]

        y_title_gap = title_gap * plot_height
        y_frame_gap = frame_gap * plot_height

        title_x = [
            x_left - x_node_width / 2,
            x_right + x_node_width / 2,
        ]

        # leftmost title
        title_lr = [0, 1] if ii == 0 else [1]

        for lr in title_lr:
            if title_side in ("top", "both"):
                if title_loc == "outer":
                    yt = min(voffset) + y_title_gap + y_frame_gap + plot_height
                elif title_loc == "inner":
                    yt = y_title_gap + node_pos_top[lr][last_label[lr]]
                ax.text(
                    title_x[lr],
                    yt,
                    titles[ii + lr],
                    {"ha": "center", "va": "bottom"},
                    fontweight=title_fontweight,
                    fontstyle=title_fontstyle,
                    fontfamily=title_fontfamily,
                    fontsize=title_fontsize,
                    color=title_fontcolor,
                )

            if title_side in ("bottom", "both"):
                if title_loc == "outer":
                    yt = min(voffset) - y_title_gap - y_frame_gap
                elif title_loc == "inner":
                    yt = voffset[ii + lr] - y_title_gap
                ax.text(
                    title_x[lr],
                    yt,
                    titles[ii + lr],
                    {"ha": "center", "va": "top"},
                    fontweight=title_fontweight,
                    fontstyle=title_fontstyle,
                    fontfamily=title_fontfamily,
                    fontsize=title_fontsize,
                    color=title_fontcolor,
                )


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
