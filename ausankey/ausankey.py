
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
        super().__init__(f"Sankey graph does not support null values.")


class LabelMismatchError(SankeyError):
    def __init__(self,side,msg):
        super().__init__(f'{side} labels and data do not match.{msg}')


def sankey(
            data,
            colorDict=None,
            aspect=4,
            labelOrder=None,
            fontsize=14,
            titles=None,
            titleGap=0.05,
            titleSide="top",  # "bottom", "both"
            frameSide="none",
            frameGap=0.1,
            labelDict=None,
            labelWidth=0,
            labelGap=0.01,
            barWidth=0.02,
            barGap=0.05,
            alpha=0.65,
            colormap="viridis",
            sorting=0,
            valign="bottom",  # "top","center"
            ax=None,
          ):
    '''
    Make Sankey Diagram with left-right flow

    Inputs:
        data = pandas dataframe of labels and weights in alternating columns
        colorDict = Dictionary of colors to use for each label
            {'label':'color'}
        left_labels = order of the left labels in the diagram
        right_labels = order of the right labels in the diagram
        aspect = vertical extent of the diagram in units of horizontal extent
        rightColor = If true, each strip in the diagram will be be colored
                    according to its left label
    Ouput:
        None
    '''

    num_col = len(data.columns)
    data.columns = range(num_col)  # force numeric column headings
    num_side = int(num_col/2)  # number of labels
    num_flow = num_side - 1

    # sizes
    weight_sum = np.empty(num_side)
    num_uniq = np.empty(num_side)
    col_hgt = np.empty(num_side)
    for ii in range(num_side):
        weight_sum[ii] = sum(data[2*ii+1])
        num_uniq[ii] = len(pd.Series(data[2*ii]).unique())

    for ii in range(num_side):
        col_hgt[ii] = weight_sum[ii] + (num_uniq[ii]-1)*barGap*max(weight_sum)

    # overall dimensions
    plot_height = max(col_hgt)
    sub_width = plot_height/aspect
    plotWidth = (
        (num_side-1)*sub_width
        + 2*sub_width*labelWidth
        + num_side*sub_width*barWidth
      )

    # offsets for alignment
    voffset = np.empty(num_side)
    if valign == "top":
        vscale = 1
    elif valign == "center":
        vscale = 0.5
    else: # bottom, or undefined
        vscale = 0

    for ii in range(num_side):
        voffset[ii] = vscale*(col_hgt[1] - col_hgt[ii])

    # labels
    label_record = data[range(0, 2*num_side, 2)].to_records(index=False)
    flattened = [item for sublist in label_record for item in sublist]
    flatcat = pd.Series(flattened).unique()

    # If no colorDict given, make one
    if colorDict is None:
        colorDict = {}
        cmap = plt.cm.get_cmap(colormap)
        color_palette = cmap(np.linspace(0, 1, len(flatcat)))
        for i, label in enumerate(flatcat):
            colorDict[label] = color_palette[i]

    # draw each segment of the graph
    if ax is None:
        ax = plt.gca()

    for ii in range(num_flow):

        _sankey(
            ii, num_flow, data,
            titles=titles,
            titleGap=titleGap,
            titleSide=titleSide,
            labelOrder=labelOrder,
            colorDict=colorDict,
            fontsize=fontsize,
            labelDict=labelDict or {},
            labelWidth=labelWidth,
            labelGap=labelGap,
            barWidth=barWidth,
            barGap=barGap,
            sub_width=sub_width,
            plot_height=plot_height,
            alpha=alpha,
            voffset=voffset,
            sorting=sorting,
            ax=ax,
        )

    # frame on top/bottom edge
    if frameSide in ("top", "both"):
        col = [0, 0, 0, 1]
    else:
        col = [1, 1, 1, 0]

    ax.plot(
        [0, plotWidth],
        min(voffset) + (plot_height) + (titleGap+frameGap)*plot_height + [0, 0],
        color=col)

    if frameSide in ("bottom", "both"):
        col = [0, 0, 0, 1]
    else:
        col = [1, 1, 1, 0]

    ax.plot(
        [0, plotWidth],
        min(voffset) - (titleGap+frameGap)*plot_height + [0, 0],
        color=col)

    # complete plot
    ax.axis('off')


def _sankey(
        ii, num_flow, data,
        colorDict=None,
        labelOrder=None,
        fontsize=None,
        titles=None,
        titleGap=None,
        titleSide=None,
        plot_height=None,
        sub_width=None,
        labelDict=None,
        labelWidth=None,
        labelGap=None,
        barWidth=None,
        barGap=None,
        alpha=None,
        voffset=None,
        sorting=None,
        ax=None,
      ):

    labelind = 2*ii
    weightind = 2*ii+1

    left = pd.Series(data[labelind])
    right = pd.Series(data[labelind+2])
    left_weight = pd.Series(data[weightind])
    right_weight = pd.Series(data[weightind+2])

    if any(left_weight.isnull()) | any(right_weight.isnull()):
        raise NullsInFrameError()

    # label order / sorting

    # calc label weight then sort
    wgt = {}
    for dd in [0, 2]:
        lbl = data[labelind+dd].unique()
        wgt[dd] = {}
        for uniq in lbl:
            ind = (data[labelind+dd] == uniq)
            wgt[dd][uniq] = data[weightind+dd][ind].sum()

        wgt[dd] = dict(sorted(
          wgt[dd].items(),
          key=lambda item: sorting*item[1]
          # sorting = 0,1,-1 affects this
        ))

    if labelOrder is not None:
        left_labels = list(labelOrder[ii])
        right_labels = list(labelOrder[ii+1])
    else:
        left_labels = list(wgt[0].keys())
        right_labels = list(wgt[2].keys())

    # check labels
    check_data_matches_labels(
      left_labels, left, 'left')
    check_data_matches_labels(
      right_labels, right, 'right')

    # check colours
    all_labels = pd.Series(np.r_[left.unique(), right.unique()]).unique()

    missing = [label for label in all_labels if label not in colorDict]
    if missing:
        msg = (
            "The colorDict parameter is missing "
            "values for the following labels: "
        )
        msg += '{}'.format(', '.join(missing))
        raise ValueError(msg)

    # Determine sizes of individual strips
    barSizeLeft = {}
    barSizeRight = {}
    for left_label in left_labels:
        barSizeLeft[left_label] = {}
        barSizeRight[left_label] = {}
        for right_label in right_labels:
            ind = (left == left_label) & (right == right_label)
            barSizeLeft[left_label][right_label] = left_weight[ind].sum()
            barSizeRight[left_label][right_label] = right_weight[ind].sum()

    # Determine positions of left label patches and total widths
    left_widths = {}
    for i, left_label in enumerate(left_labels):
        myD = {}
        myD['left'] = left_weight[left == left_label].sum()
        if i == 0:
            myD['bottom'] = voffset[ii]
        else:
            myD['bottom'] = (
                left_widths[left_labels[i-1]]['top'] + barGap*plot_height
            )
        myD['top'] = myD['bottom'] + myD['left']
        left_widths[left_label] = myD

    # Determine positions of right label patches and total widths
    right_widths = {}
    for i, right_label in enumerate(right_labels):
        myD = {}
        myD['right'] = right_weight[right == right_label].sum()
        if i == 0:
            myD['bottom'] = voffset[ii+1]
        else:
            myD['bottom'] = (
                right_widths[right_labels[i-1]]['top'] + barGap * plot_height
            )
        myD['top'] = myD['bottom'] + myD['right']
        right_widths[right_label] = myD

    # horizontal extents of flows in each subdiagram
    x_bar_width = barWidth*sub_width
    x_left = x_bar_width + labelWidth*sub_width + ii*(sub_width+x_bar_width)
    x_right = x_left + sub_width

    # Draw bars and their labels
    if ii == 0:  # first time
        for left_label in left_labels:
            lbot = left_widths[left_label]['bottom']
            lll = left_widths[left_label]['left']
            ax.fill_between(
                x_left+[-x_bar_width, 0],
                2*[lbot],
                2*[lbot + lll],
                color=colorDict[left_label],
                alpha=1,
                lw=0,
                snap=True,
            )
            ax.text(
                x_left - (labelGap+barWidth)*sub_width,
                lbot + 0.5*lll,
                labelDict.get(left_label, left_label),
                {'ha': 'right', 'va': 'center'},
                fontsize=fontsize
            )
    for right_label in right_labels:
        rbot = right_widths[right_label]['bottom']
        rrr = right_widths[right_label]['right']
        ax.fill_between(
          x_right+[0, x_bar_width],
          2*[rbot],
          [rbot + rrr],
          color=colorDict[right_label],
          alpha=1,
          lw=0,
          snap=True,
        )
        if ii < num_flow-1:  # inside labels
            ax.text(
              x_right + (labelGap+barWidth)*sub_width,
              rbot + 0.5*rrr,
              labelDict.get(right_label, right_label),
              {'ha': 'left', 'va': 'center'},
              fontsize=fontsize
            )
        if ii == num_flow-1:  # last time
            ax.text(
              x_right + (labelGap+barWidth)*sub_width,
              rbot + 0.5*rrr,
              labelDict.get(right_label, right_label),
              {'ha': 'left', 'va': 'center'},
              fontsize=fontsize
            )

    # "titles"
    if titles is not None:

        # leftmost title
        if ii == 0:
            xt = x_left - x_bar_width/2
            if titleSide in ("top", "both"):
                yt = titleGap * plot_height + left_widths[left_label]['top']
                va = 'bottom'
                ax.text(
                    xt, yt, titles[ii],
                    {'ha': 'center', 'va': va},
                    fontsize=fontsize,
                )

            if titleSide in ("bottom", "both"):
                yt = voffset[ii] - titleGap*plot_height
                va = 'top'

                ax.text(
                    xt, yt, titles[ii],
                    {'ha': 'center', 'va': va},
                    fontsize=fontsize,
                )

        # all other titles
        xt = x_right + x_bar_width/2
        if (titleSide == "top") | (titleSide == "both"):
            yt = titleGap * plot_height + right_widths[right_label]['top']

            ax.text(
                xt, yt, titles[ii+1],
                {'ha': 'center', 'va': 'bottom'},
                fontsize=fontsize,
            )

        if (titleSide == "bottom") | (titleSide == "both"):
            yt = voffset[ii+1] - titleGap*plot_height

            ax.text(
                xt, yt, titles[ii+1],
                {'ha': 'center', 'va': 'top'},
                fontsize=fontsize,
            )

    # Plot strips
    num_div = 20
    num_arr = 50
    for left_label in left_labels:
        for right_label in right_labels:

            if not any(
                  (left == left_label) & (right == right_label)):
                continue

            lbot = left_widths[left_label]['bottom']
            rbot = right_widths[right_label]['bottom']
            lbar = barSizeLeft[left_label][right_label]
            rbar = barSizeRight[left_label][right_label]

            # Create array of y values for each strip, half at left value,
            # half at right, convolve
            ys_d = np.array(num_arr*[lbot] + num_arr*[rbot])
            ys_d = np.convolve(ys_d, 1/num_div * np.ones(num_div), mode='valid')
            ys_d = np.convolve(ys_d, 1/num_div * np.ones(num_div), mode='valid')

            ys_u = np.array(num_arr * [lbot + lbar] + num_arr * [rbot + rbar])
            ys_u = np.convolve(ys_u, 1/num_div * np.ones(num_div), mode='valid')
            ys_u = np.convolve(ys_u, 1/num_div * np.ones(num_div), mode='valid')

            # Update bottom edges at each label
            # so next strip starts at the right place
            left_widths[left_label]['bottom'] += lbar
            right_widths[right_label]['bottom'] += rbar

            xx = np.linspace(x_left, x_right, len(ys_d))
            cc = combine_colours(
              colorDict[left_label],
              colorDict[right_label], len(ys_d))

            for jj in range(len(ys_d)-1):
                ax.fill_between(
                  xx[[jj, jj+1]],
                  ys_d[[jj, jj+1]],
                  ys_u[[jj, jj+1]],
                  color=cc[:, jj],
                  alpha=alpha,
                  lw=0,
                  edgecolor="none",
                  snap=True,
                )


def check_data_matches_labels(labels, data, side):
    if len(labels) > 0:
        if isinstance(data, list):
            data = set(data)
        if isinstance(data, pd.Series):
            data = set(data.unique().tolist())
        if isinstance(labels, list):
            labels = set(labels)
        if labels != data:
            msg = "\n"
            maxlen = 20
            if len(labels) <= maxlen:
                msg = "Labels: " + ",".join(labels) + "\n"
            if len(data) < maxlen:
                msg += "Data: " + ",".join(data)
            raise LabelMismatchError(side, msg)


def combine_colours(c1, c2, num_col):

    colorArrayLen = 4
    # if not [r,g,b,a] assume a hex string like "#rrggbb":

    if len(c1) != colorArrayLen:
        r1 = int(c1[1:3], 16)/255
        g1 = int(c1[3:5], 16)/255
        b1 = int(c1[5:7], 16)/255
        c1 = [r1, g1, b1, 1]

    if len(c2) != colorArrayLen:
        r2 = int(c2[1:3], 16)/255
        g2 = int(c2[3:5], 16)/255
        b2 = int(c2[5:7], 16)/255
        c2 = [r2, g2, b2, 1]

    rr = np.linspace(c1[0], c2[0], num_col)
    gg = np.linspace(c1[1], c2[1], num_col)
    bb = np.linspace(c1[2], c2[2], num_col)
    aa = np.linspace(c1[3], c2[3], num_col)

    return np.array([rr, gg, bb, aa])

