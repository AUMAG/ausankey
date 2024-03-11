
"""
Produces simple Sankey Diagrams with matplotlib.

@author: wspr

Forked from: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class SankeyException(Exception):
    pass


class NullsInFrame(SankeyException):
    pass


class LabelMismatch(SankeyException):
    pass


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
            labelDict={},
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
        leftLabels = order of the left labels in the diagram
        rightLabels = order of the right labels in the diagram
        aspect = vertical extent of the diagram in units of horizontal extent
        rightColor = If true, each strip in the diagram will be be colored
                    according to its left label
    Ouput:
        None
    '''

    NC = len(data.columns)
    data.columns = range(NC)  # force numeric column headings
    N = int(NC/2)  # number of labels
    
    # sizes
    Wsum = np.empty(N)
    Nunq = np.empty(N)
    Lhgt = np.empty(N)
    for ii in range(N):
        Wsum[ii] = sum(data[2*ii+1])
        Nunq[ii] = len(pd.Series(data[2*ii]).unique())

    for ii in range(N):
        Lhgt[ii] = Wsum[ii] + (Nunq[ii]-1)*barGap*max(Wsum)

    # overall dimensions
    plotHeight = max(Lhgt)
    subplotWidth = plotHeight/aspect
    plotWidth = (
        (N-1)*subplotWidth
        + 2*subplotWidth*labelWidth
        + N*subplotWidth*barWidth
      )

    # offsets for alignment
    voffset = np.empty(N)
    if valign == "top":
        vscale = 1
    elif valign == "center":
        vscale = 0.5
    else: # bottom, or undefined
        vscale = 0
    
    for ii in range(N):
        voffset[ii] = vscale*(Lhgt[1] - Lhgt[ii])

    # labels
    labelRec = data[range(0, 2*N, 2)].to_records(index=False)
    flattened = [item for sublist in labelRec for item in sublist]
    flatcat = pd.Series(flattened).unique()

    # If no colorDict given, make one
    if colorDict is None:
        colorDict = {}
        cmap = plt.cm.get_cmap(colormap)
        colorPalette = cmap(np.linspace(0, 1, len(flatcat)))
        for i, label in enumerate(flatcat):
            colorDict[label] = colorPalette[i]

    # draw each segment of the graph
    if ax is None:
        ax = plt.gca()

    for ii in range(N-1):

        _sankey(
            ii, N-1, data,
            Wsum=Wsum,
            titles=titles,
            titleGap=titleGap,
            titleSide=titleSide,
            labelOrder=labelOrder,
            colorDict=colorDict,
            aspect=aspect,
            fontsize=fontsize,
            labelDict=labelDict,
            labelWidth=labelWidth,
            labelGap=labelGap,
            barWidth=barWidth,
            barGap=barGap,
            plotWidth=plotWidth,
            subplotWidth=subplotWidth,
            plotHeight=plotHeight,
            alpha=alpha,
            valign=valign,
            Lhgt=Lhgt,
            voffset=voffset,
            sorting=sorting,
            ax=ax,
        )

    # frame on top/bottom edge
    if (frameSide == "top") | (frameSide == "both"):
        col = [0, 0, 0, 1]
    else:
        col = [1, 1, 1, 0]

    ax.plot(
        [0, plotWidth],
        min(voffset) + (plotHeight) + (titleGap+frameGap)*plotHeight + [0, 0],
        color=col)

    if (frameSide == "bottom") | (frameSide == "both"):
        col = [0, 0, 0, 1]
    else:
        col = [1, 1, 1, 0]

    ax.plot(
        [0, plotWidth],
        min(voffset) - (titleGap+frameGap)*plotHeight + [0, 0],
        color=col)

    # complete plot
    ax.axis('off')


def _sankey(
        ii, N, data,
        Wsum=None,
        colorDict=None,
        labelOrder=None,
        aspect=4,
        fontsize=14,
        figureName=None,
        closePlot=False,
        titles=None,
        titleGap=0,
        titleSide="",
        plotWidth=0,
        plotHeight=0,
        subplotWidth=0,
        labelDict={},
        labelWidth=0,
        labelGap=0,
        barWidth=0,
        barGap=0,
        alpha=0,
        valign=None,
        Lhgt=0,
        voffset=None,
        sorting=0,
        ax=None,
      ):

    labelind = 2*ii
    weightind = 2*ii+1

    left = pd.Series(data[labelind])
    right = pd.Series(data[labelind+2])
    leftWeight = pd.Series(data[weightind])
    rightWeight = pd.Series(data[weightind+2])

    if any(leftWeight.isnull()) | any(rightWeight.isnull()):
        raise NullsInFrame('Sankey graph does not support null values.')

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
        leftLabels = list(labelOrder[ii])
        rightLabels = list(labelOrder[ii+1])
    else:
        leftLabels = list(wgt[0].keys())
        rightLabels = list(wgt[2].keys())

    # check labels
    check_data_matches_labels(
      leftLabels, left, 'left')
    check_data_matches_labels(
      rightLabels, right, 'right')

    # check colours
    allLabels = pd.Series(np.r_[left.unique(), right.unique()]).unique()

    missing = [label for label in allLabels if label not in colorDict.keys()]
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
    for leftLabel in leftLabels:
        barSizeLeft[leftLabel] = {}
        barSizeRight[leftLabel] = {}
        for rightLabel in rightLabels:
            ind = (left == leftLabel) & (right == rightLabel)
            barSizeLeft[leftLabel][rightLabel] = leftWeight[ind].sum()
            barSizeRight[leftLabel][rightLabel] = rightWeight[ind].sum()

    # Determine positions of left label patches and total widths
    leftWidths = {}
    for i, leftLabel in enumerate(leftLabels):
        myD = {}
        myD['left'] = leftWeight[left == leftLabel].sum()
        if i == 0:
            myD['bottom'] = voffset[ii]
        else:
            myD['bottom'] = (
                leftWidths[leftLabels[i-1]]['top'] + barGap*plotHeight
            )
        myD['top'] = myD['bottom'] + myD['left']
        leftWidths[leftLabel] = myD

    # Determine positions of right label patches and total widths
    rightWidths = {}
    for i, rightLabel in enumerate(rightLabels):
        myD = {}
        myD['right'] = rightWeight[right == rightLabel].sum()
        if i == 0:
            myD['bottom'] = voffset[ii+1]
        else:
            myD['bottom'] = (
                rightWidths[rightLabels[i-1]]['top'] + barGap * plotHeight
            )
        myD['top'] = myD['bottom'] + myD['right']
        rightWidths[rightLabel] = myD

    # horizontal extents of flows in each subdiagram
    xMax = subplotWidth
    barW = barWidth*xMax
    xLeft = barW + labelWidth*xMax + ii*(xMax+barW)
    xRight = xLeft + xMax

    # Draw bars and their labels
    if ii == 0:  # first time
        for leftLabel in leftLabels:
            lbot = leftWidths[leftLabel]['bottom']
            lll = leftWidths[leftLabel]['left']
            ax.fill_between(
                xLeft+[-barW, 0],
                2*[lbot],
                2*[lbot + lll],
                color=colorDict[leftLabel],
                alpha=1,
                lw=0,
                snap=True,
            )
            ax.text(
                xLeft - (labelGap+barWidth)*xMax,
                lbot + 0.5*lll,
                labelDict.get(leftLabel, leftLabel),
                {'ha': 'right', 'va': 'center'},
                fontsize=fontsize
            )
    for rightLabel in rightLabels:
        rbot = rightWidths[rightLabel]['bottom']
        rrr = rightWidths[rightLabel]['right']
        ax.fill_between(
          xRight+[0, barW],
          2*[rbot],
          [rbot + rrr],
          color=colorDict[rightLabel],
          alpha=1,
          lw=0,
          snap=True,
        )
        if ii < N-1:  # inside labels
            ax.text(
              xRight + (labelGap+barWidth)*xMax,
              rbot + 0.5*rrr,
              labelDict.get(rightLabel, rightLabel),
              {'ha': 'left', 'va': 'center'},
              fontsize=fontsize
            )
        if ii == N-1:  # last time
            ax.text(
              xRight + (labelGap+barWidth)*xMax,
              rbot + 0.5*rrr,
              labelDict.get(rightLabel, rightLabel),
              {'ha': 'left', 'va': 'center'},
              fontsize=fontsize
            )

    # "titles"
    if titles is not None:

        # leftmost title
        if ii == 0:
            xt = xLeft - xMax*barWidth/2
            if ((titleSide == "top") or (titleSide == "both")):
                yt = titleGap * plotHeight + leftWidths[leftLabel]['top']
                va = 'bottom'
                ax.text(
                    xt, yt, titles[ii],
                    {'ha': 'center', 'va': va},
                    fontsize=fontsize,
                )

            if (titleSide == "bottom") | (titleSide == "both"):
                yt = voffset[ii] - titleGap*plotHeight
                va = 'top'

                ax.text(
                    xt, yt, titles[ii],
                    {'ha': 'center', 'va': va},
                    fontsize=fontsize,
                )

        # all other titles
        xt = xRight + xMax*barWidth/2
        if (titleSide == "top") | (titleSide == "both"):
            yt = titleGap * plotHeight + rightWidths[rightLabel]['top']

            ax.text(
                xt, yt, titles[ii+1],
                {'ha': 'center', 'va': 'bottom'},
                fontsize=fontsize,
            )

        if (titleSide == "bottom") | (titleSide == "both"):
            yt = voffset[ii+1] - titleGap*plotHeight

            ax.text(
                xt, yt, titles[ii+1],
                {'ha': 'center', 'va': 'top'},
                fontsize=fontsize,
            )

    # Plot strips
    Ndiv = 20
    Narr = 50
    for leftLabel in leftLabels:
        for rightLabel in rightLabels:

            if not any(
                  (left == leftLabel) & (right == rightLabel)):
                continue

            lbot = leftWidths[leftLabel]['bottom']
            rbot = rightWidths[rightLabel]['bottom']
            lbar = barSizeLeft[leftLabel][rightLabel]
            rbar = barSizeRight[leftLabel][rightLabel]

            # Create array of y values for each strip, half at left value,
            # half at right, convolve
            ys_d = np.array(Narr*[lbot] + Narr*[rbot])
            ys_d = np.convolve(ys_d, 1/Ndiv * np.ones(Ndiv), mode='valid')
            ys_d = np.convolve(ys_d, 1/Ndiv * np.ones(Ndiv), mode='valid')

            ys_u = np.array(Narr * [lbot + lbar] + Narr * [rbot + rbar])
            ys_u = np.convolve(ys_u, 1/Ndiv * np.ones(Ndiv), mode='valid')
            ys_u = np.convolve(ys_u, 1/Ndiv * np.ones(Ndiv), mode='valid')

            # Update bottom edges at each label
            # so next strip starts at the right place
            leftWidths[leftLabel]['bottom'] += lbar
            rightWidths[rightLabel]['bottom'] += rbar

            xx = np.linspace(xLeft, xRight, len(ys_d))
            cc = combineColours(
              colorDict[leftLabel],
              colorDict[rightLabel], len(ys_d))

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
            if len(labels) <= 20:
                msg = "Labels: " + ",".join(labels) + "\n"
            if len(data) < 20:
                msg += "Data: " + ",".join(data)
            raise LabelMismatch(
              '{0} labels and data do not match.{1}'.format(side, msg))


def combineColours(c1, c2, N):
    if len(c1) != 4:
        r1 = int(c1[1:3], 16)/255
        g1 = int(c1[3:5], 16)/255
        b1 = int(c1[5:7], 16)/255
        c1 = [r1, g1, b1, 1]

    if len(c2) != 4:
        r2 = int(c2[1:3], 16)/255
        g2 = int(c2[3:5], 16)/255
        b2 = int(c2[5:7], 16)/255
        c2 = [r2, g2, b2, 1]

    rr = np.linspace(c1[0], c2[0], N)
    gg = np.linspace(c1[1], c2[1], N)
    bb = np.linspace(c1[2], c2[2], N)
    aa = np.linspace(c1[3], c2[3], N)

    return np.array([rr, gg, bb, aa])

