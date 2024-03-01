# -*- coding: utf-8 -*-
"""
Produces simple Sankey Diagrams with matplotlib.
@author: Anneya Golob & marcomanz & pierre-sassoulas & jorwoods
                      .-.
                 .--.(   ).--.
      <-.  .-.-.(.->          )_  .--.
       `-`(     )-'             `)    )
         (o  o  )                `)`-'
        (      )                ,)
        ( ()  )                 )
         `---"\    ,    ,    ,/`
               `--' `--' `--'
                |  |   |   |
                |  |   |   |
                '  |   '   |
"""

from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PySankeyException(Exception):
    pass


class NullsInFrame(PySankeyException):
    pass


class LabelMismatch(PySankeyException):
    pass


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
            raise LabelMismatch('{0} labels and data do not match.{1}'.format(side, msg))


def sankey(data, colorDict=None,
           aspect=4, rightColor=False,
           labelOrder=None,
           fontsize=14, figureName=None, closePlot=False, titles=None, labelDict={},labelWidth=0,colormap="viridis",sorting=0):
    '''
    Make Sankey Diagram showing flow from left-->right

    Inputs:
        left = NumPy array of object labels on the left of the diagram
        right = NumPy array of corresponding labels on the right of the diagram
            len(right) == len(left)
        leftWeight = NumPy array of weights for each strip starting from the
            left of the diagram, if not specified 1 is assigned
        rightWeight = NumPy array of weights for each strip starting from the
            right of the diagram, if not specified the corresponding leftWeight
            is assigned
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
 
    plt.figure()
    plt.rc('text', usetex=False)
    plt.rc('font', family='sans')    
    
    N = int(len(data.columns)/2) # number of labels
    
    # sizes
    Wsum = np.empty(N-1)
    for ii in range(N-1):
      Wsum[ii] = sum(data[2*ii+1])
    plotHeight = max(Wsum)
    subplotWidth = plotHeight/aspect
    plotWidth = subplotWidth*(N-1) + 2*subplotWidth*labelWidth

    # labels
    labelRec = data[range(0,2*N,2)].to_records(index=False)
    flattened = [item for sublist in labelRec for item in sublist]
    flatcat = pd.Series(flattened).unique()
    
    # If no colorDict given, make one
    if colorDict is None:
      colorDict = {}
      cmap = plt.cm.get_cmap(colormap)
      colorPalette = cmap(np.linspace(0,1,len(flatcat)))
      for i, label in enumerate(flatcat):
        colorDict[label] = colorPalette[i]

    for ii in range(N-1):
      _sankey(ii,N-1,data, 
           Wsum=Wsum,
           titles=titles,
           labelOrder=labelOrder, 
           colorDict=colorDict,
           aspect=aspect, 
           rightColor=rightColor,
           fontsize=fontsize, 
           figureName=figureName, 
           closePlot=closePlot, 
           labelDict=labelDict,
           labelWidth=labelWidth,
           plotWidth=plotWidth,
           subplotWidth=subplotWidth,
           plotHeight=plotHeight,
           sorting=sorting)
    
    # frame on bottom edge; might delete
    plt.plot([0,plotWidth],-0.1*max(Wsum)+[0,0])
    
    
    plt.gca().axis('off')
    plt.gcf().set_size_inches(6, 6)
    
    if figureName != None:
        plt.savefig("{}.png".format(figureName), bbox_inches='tight', dpi=150)
    
    if closePlot:
        plt.close()



def _sankey(ii,N,data, 
           Wsum=None,
           colorDict=None,
           labelOrder=None,
           aspect=4, 
           rightColor=False,
           fontsize=14, 
           figureName=None, 
           closePlot=False, 
           titles=None, 
           plotWidth=0,
           plotHeight=0,
           subplotWidth=0,
           labelDict={},
           labelWidth=0,
           sorting=0):         
    
    labelind = 2*ii
    weightind = 2*ii+1
    
    left  = list(data[labelind])
    right = list(data[labelind+2])
    leftWeight  = list(data[weightind])
    rightWeight = list(data[weightind+2])
    
    # Check weights
    if len(leftWeight) == 0:
        leftWeight = np.ones(len(left))
    if len(rightWeight) == 0:
        rightWeight = leftWeight

    # Create Dataframe
    if isinstance(left, pd.Series):
        left = left.reset_index(drop=True)
    if isinstance(right, pd.Series):
        right = right.reset_index(drop=True)
    dataFrame = pd.DataFrame({
      'left': left, 
      'right': right, 
      'leftWeight': leftWeight,
      'rightWeight': rightWeight}, index=range(len(left)))

    if len(dataFrame[(dataFrame.left.isnull()) | (dataFrame.right.isnull())]):
        raise NullsInFrame('Sankey graph does not support null values.')

    # label order / sorting
    if labelOrder is not None:
      leftLabels  = list(labelOrder[ii])
      rightLabels = list(labelOrder[ii+1])
    else:
      leftLabels = None
      rightLabels = None
    
    wgt = {}
    for dd in [0,2]:
      lbl = data[labelind+dd].unique()
      wgt[dd] = {}
      for uniq in lbl:
        ind = (data[labelind+dd] == uniq)
        wgt[dd][uniq] = data[weightind+dd][ind].sum()
      wgt[dd] = dict(sorted(
        wgt[dd].items(),
        key=lambda item: sorting*item[1]
      ))
    
    if leftLabels == None:
      leftLabels  = list(wgt[0].keys())
    if rightLabels == None:
      rightLabels = list(wgt[2].keys())
    
    # check labels
    check_data_matches_labels(
      leftLabels, dataFrame['left'], 'left')
    check_data_matches_labels(
      rightLabels, dataFrame['right'], 'right')
      
    # Identify all labels that appear 'left' or 'right'
    allLabels = pd.Series(np.r_[dataFrame.left.unique(), dataFrame.right.unique()]).unique()
    
    # check colours
    missing = [label for label in allLabels if label not in colorDict.keys()]
    if missing:
      msg = "The colorDict parameter is missing values for the following labels : "
      msg += '{}'.format(', '.join(missing))
      raise ValueError(msg)

    # Determine widths of individual strips
    ns_l = defaultdict()
    ns_r = defaultdict()
    for leftLabel in leftLabels:
        leftDict = {}
        rightDict = {}
        for rightLabel in rightLabels:
            leftind = (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
            rightind = (dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)
            leftDict[rightLabel] = dataFrame[leftind].leftWeight.sum()
            rightDict[rightLabel] = dataFrame[rightind].rightWeight.sum()
        ns_l[leftLabel] = leftDict
        ns_r[leftLabel] = rightDict

    # Determine positions of left label patches and total widths
    leftWidths = defaultdict()
    for i, leftLabel in enumerate(leftLabels):
        myD = {}
        myD['left'] = dataFrame[dataFrame.left == leftLabel].leftWeight.sum()
        if i == 0:
            myD['bottom'] = 0
            myD['top'] = myD['left']
        else:
            myD['bottom'] = leftWidths[leftLabels[i - 1]]['top'] + 0.02 * dataFrame.leftWeight.sum()
            myD['top'] = myD['bottom'] + myD['left']
        leftWidths[leftLabel] = myD

    # Determine positions of right label patches and total widths
    rightWidths = defaultdict()
    for i, rightLabel in enumerate(rightLabels):
        myD = {}
        myD['right'] = dataFrame[dataFrame.right == rightLabel].rightWeight.sum()
        if i == 0:
            myD['bottom'] = 0
            myD['top'] = myD['right']
        else:
            myD['bottom'] = rightWidths[rightLabels[i - 1]]['top'] + 0.02 * dataFrame.rightWeight.sum()
            myD['top'] = myD['bottom'] + myD['right']
        rightWidths[rightLabel] = myD

    # horizontal extents of diagram
    xMax = subplotWidth
    xLeft = labelWidth*xMax + ii*xMax
    xRight = labelWidth*xMax + (ii+1)*xMax

    # Draw vertical bars on left and right of each  label's section & print label
    for leftLabel in leftLabels:
        plt.fill_between(
            xLeft+[-0.02 * xMax, 0],
            2 * [leftWidths[leftLabel]['bottom']],
            2 * [leftWidths[leftLabel]['bottom'] + leftWidths[leftLabel]['left']],
            color=colorDict[leftLabel],
            alpha=0.99
        )
        if ii == 0: # first time
          plt.text(
            xLeft - 0.05 * xMax,
            leftWidths[leftLabel]['bottom'] + 0.5 * leftWidths[leftLabel]['left'],
            labelDict.get(leftLabel,leftLabel),
            {'ha': 'right', 'va': 'center'},
            fontsize=fontsize
          )
    for rightLabel in rightLabels:
        plt.fill_between(
            xRight+[0, 0.02 * xMax], 2 * [rightWidths[rightLabel]['bottom']],
            2 * [rightWidths[rightLabel]['bottom'] + rightWidths[rightLabel]['right']],
            color=colorDict[rightLabel],
            alpha=0.99
        )
        if ii == N-1: # last time
          plt.text(
            xRight + 0.05 * xMax,
            rightWidths[rightLabel]['bottom'] + 0.5 * rightWidths[rightLabel]['right'],
            labelDict.get(rightLabel,rightLabel),
            {'ha': 'left', 'va': 'center'},
            fontsize=fontsize
          )
    
    # "titles"
    if titles is not None:
      if ii == 0:
        plt.text(
          -xMax*0.01 + xLeft, 
          1.05*(leftWidths[leftLabel]['bottom'] + leftWidths[leftLabel]['left']),
          titles[ii],
          {'ha': 'center', 'va': 'center'},
          fontsize = fontsize,
        )
      
      plt.text(
        xRight + xMax*0.01, 
        1.05*(rightWidths[rightLabel]['bottom'] + rightWidths[rightLabel]['right']),
        titles[ii+1],
        {'ha': 'center', 'va': 'center'},
        fontsize = fontsize,
      )

    # Plot strips
    for leftLabel in leftLabels:
        for rightLabel in rightLabels:
            labelColor = leftLabel
            if rightColor:
                labelColor = rightLabel
            if len(dataFrame[(dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)]) > 0:
                # Create array of y values for each strip, half at left value,
                # half at right, convolve
                ys_d = np.array(50 * [leftWidths[leftLabel]['bottom']] + 50 * [rightWidths[rightLabel]['bottom']])
                ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode='valid')
                ys_d = np.convolve(ys_d, 0.05 * np.ones(20), mode='valid')
                ys_u = np.array(50 * [leftWidths[leftLabel]['bottom'] + ns_l[leftLabel][rightLabel]] + 50 * [rightWidths[rightLabel]['bottom'] + ns_r[leftLabel][rightLabel]])
                ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode='valid')
                ys_u = np.convolve(ys_u, 0.05 * np.ones(20), mode='valid')

                # Update bottom edges at each label so next strip starts at the right place
                leftWidths[leftLabel]['bottom'] += ns_l[leftLabel][rightLabel]
                rightWidths[rightLabel]['bottom'] += ns_r[leftLabel][rightLabel]
                plt.fill_between(
                    np.linspace(xLeft, xRight, len(ys_d)), ys_d, ys_u, alpha=0.65,
                    color=colorDict[labelColor]
                )
    
    
    # frame on bottom edge; might delete
    plt.plot([xLeft,xRight],-0.05*plotHeight+[0,0])
    

