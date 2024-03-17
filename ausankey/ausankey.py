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


class NullsInFrameError(SankeyError):
    def __init__(self):
        super().__init__("Sankey graph does not support null values.")


class LabelMismatchError(SankeyError):
    def __init__(self, side, msg):
        super().__init__(f"{side} labels and data do not match.{msg}")


def sankey(
    data,
    aspect=4,
    alpha=0.65,
    ax=None,
    bar_width=0.02,
    bar_gap=0.05,
    color_dict=None,
    colormap="viridis",
    fontsize=14,
    frame_side="none",
    frame_gap=0.1,
    frame_color=None,
    label_order=None,
    label_dict=None,
    label_width=0,
    label_gap=0.01,
    titles=None,
    title_gap=0.05,
    title_side="top",  # "bottom", "both"
    sorting=0,
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

    bar_width : float
        Normalised horizontal width of the data bars
        (1.0 = 100% of plot width)

    bar_gap : float
        Normalised vertical gap between successive data bars
        (1.0 = 100% of nominal plot height).

    color_dict : dict
        Dictionary of colors to use for each label `{'label': 'color'}`

    colormap : str
        Matplotlib colormap name to automatically assign colours.
        `color_dict` can overide these on an individual basis if needed

    fontsize : int
        Font size of labels

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

    sorting : int
        Parity bit for how to sort the display of the data.
        `0` is unsorted — display data in order it appears in the DataFrame.
        `1` and `-1` sort high to low or vice versa.

    titles : list of str
        Array of title strings for each columns

    title_gap : float
        Normalised vertical gap between the column and the title string
        (1.0 = 100% of plot height)

    title_side : str
        Whether to place the titles above or below the plot.
        Allowed values: `"top"`, `"bottom"`, or `"both"`

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
    for ii in range(num_side):
        weight_sum[ii] = data[2 * ii + 1].sum()
        num_uniq[ii] = len(pd.Series(data[2 * ii]).unique())

    for ii in range(num_side):
        col_hgt[ii] = weight_sum[ii] + (num_uniq[ii] - 1) * bar_gap * max(weight_sum)

    # overall dimensions
    plot_height = max(col_hgt)
    sub_width = plot_height / aspect
    plot_width = (num_side - 1) * sub_width + 2 * sub_width * label_width + num_side * sub_width * bar_width

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

    # draw each segment of the graph
    ax = ax or plt.gca()

    for ii in range(num_flow):
        _sankey(
            ii,
            num_flow,
            data,
            titles=titles,
            title_gap=title_gap,
            title_side=title_side,
            label_order=label_order,
            color_dict=color_dict_new,
            fontsize=fontsize,
            label_dict=label_dict or {},
            label_width=label_width,
            label_gap=label_gap,
            bar_width=bar_width,
            bar_gap=bar_gap,
            sub_width=sub_width,
            plot_height=plot_height,
            alpha=alpha,
            voffset=voffset,
            sorting=sorting,
            ax=ax,
        )

    frame_top = frame_side in ("top", "both")
    frame_bot = frame_side in ("bottom", "both")

    # frame on top/bottom edge
    frame_color = frame_color or [0, 0, 0, 1]

    y_frame_gap = (title_gap + frame_gap) * plot_height

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

    # complete plot
    ax.axis("off")


###########################################


def _sankey(
    ii,
    num_flow,
    data,
    color_dict=None,
    label_order=None,
    fontsize=None,
    titles=None,
    title_gap=None,
    title_side=None,
    plot_height=None,
    sub_width=None,
    label_dict=None,
    label_width=None,
    label_gap=None,
    bar_width=None,
    bar_gap=None,
    alpha=None,
    voffset=None,
    sorting=None,
    ax=None,
):
    """Subroutine for plotting horizontal sections of the Sankey plot

    Some special-casing is used for plotting/labelling differently
    for the first and last cases.
    """
    labelind = 2 * ii
    weightind = 2 * ii + 1

    labels_lr = [pd.Series(data[labelind]), pd.Series(data[labelind + 2])]
    weights_lr = [
        pd.Series(data[weightind]),
        pd.Series(data[weightind + 2]),
    ]

    notnull = labels_lr[0].notnull() & labels_lr[1].notnull()
    labels_lr[0] = labels_lr[0][notnull]
    labels_lr[1] = labels_lr[1][notnull]
    weights_lr[0] = weights_lr[0][notnull]
    weights_lr[1] = weights_lr[1][notnull]

    if any(weights_lr[0].isnull()) | any(weights_lr[1].isnull()):
        raise NullsInFrameError

    # label order / sorting

    if label_order is not None:
        bar_lr = [
            list(label_order[ii]),
            list(label_order[ii + 1]),
        ]
    else:
        bar_lr = [
            weighted_sort(labels_lr[0], weights_lr[0], sorting),
            weighted_sort(labels_lr[1], weights_lr[1], sorting),
        ]

    # check labels
    check_data_matches_labels(bar_lr[0], labels_lr[0], "left")
    check_data_matches_labels(bar_lr[1], labels_lr[1], "right")

    # check colours
    all_labels = pd.Series([*labels_lr[0], *labels_lr[1]]).unique()
    missing = [label for label in all_labels if label not in color_dict]
    if missing:
        msg = "The color_dict parameter is missing " "values for the following labels: "
        msg += "{}".format(", ".join(missing))
        raise ValueError(msg)

    # Determine sizes of individual strips
    barsize = [{}, {}]
    for lbl_l in bar_lr[0]:
        barsize[0][lbl_l] = {}
        barsize[1][lbl_l] = {}
        for lbl_r in bar_lr[1]:
            ind = (labels_lr[0] == lbl_l) & (labels_lr[1] == lbl_r)
            barsize[0][lbl_l][lbl_r] = weights_lr[0][ind].sum()
            barsize[1][lbl_l][lbl_r] = weights_lr[1][ind].sum()

    # Determine positions of label patches and total widths
    y_bar_gap = bar_gap * plot_height

    barpos = [{}, {}]
    for lr in [0, 1]:
        for i, label in enumerate(bar_lr[lr]):
            barpos[lr][label] = {}
            barpos[lr][label]["tot"] = weights_lr[lr][labels_lr[lr] == label].sum()
            barpos[lr][label]["bot"] = voffset[ii + lr] if i == 0 else barpos[lr][bar_lr[lr][i - 1]]["top"] + y_bar_gap
            barpos[lr][label]["top"] = barpos[lr][label]["bot"] + barpos[lr][label]["tot"]

    # horizontal extents of flows in each subdiagram
    x_bar_width = bar_width * sub_width
    x_label_width = label_width * sub_width
    x_label_gap = label_gap * sub_width
    x_left = x_bar_width + x_label_gap + x_label_width + ii * (sub_width + x_bar_width)
    x_right = x_left + sub_width

    # Draw bars and their labels
    
    def draw_bar(x, y, dy, label):
        ax.fill_between(
            [x, x + x_bar_width],
            y,
            y + dy,
            color=color_dict[label],
            alpha=1,
            lw=0,
            snap=True,
        )
    if ii == 0:  # first time
        for label in bar_lr[0]:
            lbot = barpos[0][label]["bot"]
            lll = barpos[0][label]["tot"]
            draw_bar(x_left - x_bar_width, lbot, lll, label)
            
            ax.text(
                x_left - x_label_gap - x_bar_width,
                lbot + lll / 2,
                label_dict.get(label, label),
                {"ha": "right", "va": "center"},
                fontsize=fontsize,
            )
    for label in bar_lr[1]:
        rbot = barpos[1][label]["bot"]
        rrr = barpos[1][label]["tot"]
        draw_bar(x_right, rbot, rrr, label)
        
        if ii < num_flow - 1:  # inside labels
            ax.text(
                x_right + x_label_gap + x_bar_width,
                rbot + rrr / 2,
                label_dict.get(label, label),
                {"ha": "left", "va": "center"},
                fontsize=fontsize,
            )
        if ii == num_flow - 1:  # last time
            ax.text(
                x_right + x_label_gap + x_bar_width,
                rbot + rrr / 2,
                label_dict.get(label, label),
                {"ha": "left", "va": "center"},
                fontsize=fontsize,
            )

    # "titles"
    if titles is not None:
        y_title_gap = title_gap * plot_height

        # leftmost title
        if ii == 0:
            xt = x_left - x_bar_width / 2
            if title_side in ("top", "both"):
                yt = y_title_gap + barpos[0][lbl_l]["top"]
                va = "bottom"
                ax.text(
                    xt,
                    yt,
                    titles[ii],
                    {"ha": "center", "va": va},
                    fontsize=fontsize,
                )

            if title_side in ("bottom", "both"):
                yt = voffset[ii] - y_title_gap
                va = "top"
                ax.text(
                    xt,
                    yt,
                    titles[ii],
                    {"ha": "center", "va": va},
                    fontsize=fontsize,
                )

        # all other titles
        xt = x_right + x_bar_width / 2
        if title_side in ("top", "both"):
            yt = y_title_gap + barpos[1][lbl_r]["top"]
            ax.text(
                xt,
                yt,
                titles[ii + 1],
                {"ha": "center", "va": "bottom"},
                fontsize=fontsize,
            )

        if title_side in ("bottom", "both"):
            yt = voffset[ii + 1] - y_title_gap
            ax.text(
                xt,
                yt,
                titles[ii + 1],
                {"ha": "center", "va": "top"},
                fontsize=fontsize,
            )

    # Plot strips
    for lbl_l in bar_lr[0]:
        for lbl_r in bar_lr[1]:
            lind = labels_lr[0] == lbl_l
            rind = labels_lr[1] == lbl_r

            if not any(lind & rind):
                continue

            lbot = barpos[0][lbl_l]["bot"]
            rbot = barpos[1][lbl_r]["bot"]
            lbar = barsize[0][lbl_l][lbl_r]
            rbar = barsize[1][lbl_l][lbl_r]

            ys_d = create_curve(lbot, rbot)
            ys_u = create_curve(lbot + lbar, rbot + rbar)

            # Update bottom edges at each label
            # so next strip starts at the right place
            barpos[0][lbl_l]["bot"] += lbar
            barpos[1][lbl_r]["bot"] += rbar

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


###########################################


def weighted_sort(lbl, wgt, sorting):
    """creates a sorted list of labels by their summed weights"""

    arr = {}
    for uniq in lbl.unique():
        arr[uniq] = wgt[lbl == uniq].sum()

    sort_arr = sorted(
        arr.items(),
        key=lambda item: sorting * item[1],
        # sorting = 0,1,-1 affects this
    )

    return list(dict(sort_arr))


###########################################


def check_data_matches_labels(labels, data, side):
    """Consistency check of label data.

    Ensures after filtering and sorting,
    or manually specifying the label order,
    that the order of labels is still consistent
    with the labels in the data.
    """

    if len(labels) == 0:
        msg = "Length of labels equals zero?"
        raise LabelMismatchError(side, msg)

    if set(labels) != set(data):
        msg = "\n"
        maxlen = 20
        if len(labels) <= maxlen:
            msg += "Labels: " + ",".join(labels) + "\n"
        if len(data) < maxlen:
            msg += "Data: " + ",".join(data)
        raise LabelMismatchError(side, msg)


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
