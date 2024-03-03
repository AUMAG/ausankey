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


def sankey(
           data, 
           colorDict=None,
           aspect=4, 
           labelOrder=None,
           fontsize=14, 
           figureName=None, 
           closePlot=False, 
           titles=None, 
           titleGap=0.05,
           titleTop=True,
           labelDict={},
           labelWidth=0,
           barWidth=0.02,
           barGap=0.05,
           alpha=0.65,
           colormap="viridis",
           sorting=0,
           axis=False,
          ):
    '''
    Make Sankey Diagram showing flow from left-->right

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
 

    plt.figure(dpi=600)
    plt.rc('text', usetex=False)
    plt.rc('font', family='sans')    


    
    N = int(len(data.columns)/2) # number of labels
    
    # sizes
    Wsum = np.empty(N-1)
    for ii in range(N-1):
      Wsum[ii] = sum(data[2*ii+1])
    plotHeight = max(Wsum)
    subplotWidth = plotHeight/aspect
    plotWidth = (N-1)*subplotWidth + 2*subplotWidth*labelWidth + N*subplotWidth*barWidth

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
           titleGap=titleGap,
           titleTop=titleTop,
           labelOrder=labelOrder, 
           colorDict=colorDict,
           aspect=aspect, 
           fontsize=fontsize, 
           figureName=figureName, 
           closePlot=closePlot, 
           labelDict=labelDict,
           labelWidth=labelWidth,
           barWidth=barWidth,
           barGap=barGap,
           plotWidth=plotWidth,
           subplotWidth=subplotWidth,
           plotHeight=plotHeight,
           alpha=alpha,
           axis=axis,
           sorting=sorting)
    
    # axis on bottom edge
    if axis:
        col = [0,0,0,1]
    else:
        col = [1,1,1,0]
    plt.plot(
          [0,plotWidth],
          -titleGap*plotHeight+[0,0],
          color=col)
    
    plt.gca().axis('off')
    #plt.gcf().set_size_inches(6, 6)
    
    if figureName != None:
        plt.savefig("{}.png".format(figureName), bbox_inches='tight', dpi=150)
    
    if closePlot:
        plt.close()



def combineColours(c1,c2,N):
  if len(c1) != 4:
    r1 = int(c1[1:3], 16)/255
    g1 = int(c1[3:5], 16)/255
    b1 = int(c1[5:7], 16)/255
    c1 = [r1,g1,b1,1]
    
  if len(c2) != 4:
    r2 = int(c2[1:3], 16)/255
    g2 = int(c2[3:5], 16)/255
    b2 = int(c2[5:7], 16)/255
    c2 = [r2,g2,b2,1]

  rr = np.linspace(c1[0],c2[0],N)
  gg = np.linspace(c1[1],c2[1],N)
  bb = np.linspace(c1[2],c2[2],N)
  aa = np.linspace(c1[3],c2[3],N)
  
  return np.array([rr,gg,bb,aa])



def _sankey(ii,N,data, 
           Wsum=None,
           colorDict=None,
           labelOrder=None,
           aspect=4, 
           fontsize=14, 
           figureName=None, 
           closePlot=False, 
           titles=None, 
           titleGap=0,
           titleTop=True,
           plotWidth=0,
           plotHeight=0,
           subplotWidth=0,
           labelDict={},
           labelWidth=0,
           barWidth=0,
           barGap=0,
           alpha=0,
           axis=1,
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
            myD['bottom'] = leftWidths[leftLabels[i - 1]]['top'] + barGap*plotHeight
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
            myD['bottom'] = rightWidths[rightLabels[i - 1]]['top'] + barGap*plotHeight
            myD['top'] = myD['bottom'] + myD['right']
        rightWidths[rightLabel] = myD

    # horizontal extents of diagram
    xMax = subplotWidth
    xLeft = barWidth*xMax + labelWidth*xMax + ii*xMax
    xRight = labelWidth*xMax + (ii+1)*xMax

    # Draw vertical bars on left and right of each  label's section & print label
    for leftLabel in leftLabels:
      if ii == 0: # first time
        plt.fill_between(
            xLeft+[-barWidth * xMax, 0],
            2 * [leftWidths[leftLabel]['bottom']],
            2 * [leftWidths[leftLabel]['bottom'] + leftWidths[leftLabel]['left']],
            color=colorDict[leftLabel],
            alpha=1,
            lw=0,
            snap=True,
        )
        plt.text(
            xLeft - 1.5*barWidth*xMax,
            leftWidths[leftLabel]['bottom'] + 0.5 * leftWidths[leftLabel]['left'],
            labelDict.get(leftLabel,leftLabel),
            {'ha': 'right', 'va': 'center'},
            fontsize=fontsize
        )
    for rightLabel in rightLabels:
        plt.fill_between(
            xRight+[0, barWidth * xMax], 2 * [rightWidths[rightLabel]['bottom']],
            2 * [rightWidths[rightLabel]['bottom'] + rightWidths[rightLabel]['right']],
            color=colorDict[rightLabel],
            alpha=1,
            lw=0,
            snap=True,
        )
        if ii == N-1: # last time
          plt.text(
            xRight + 1.5*barWidth * xMax,
            rightWidths[rightLabel]['bottom'] + 0.5 * rightWidths[rightLabel]['right'],
            labelDict.get(rightLabel,rightLabel),
            {'ha': 'left', 'va': 'center'},
            fontsize=fontsize
          )
    
    # "titles"
    if titles is not None:

      if axis:
          yscale = 2
      else:
          yscale = 1
          
      if ii == 0:
          
        xt = -xMax*barWidth/2 + xLeft
        if titleTop:
          yt = titleGap*plotHeight +(leftWidths[leftLabel]['bottom'] + leftWidths[leftLabel]['left'])
          va = 'bottom'
        else:
          yt = -yscale*titleGap*plotHeight
          va = 'top'
        
        plt.text(xt, yt, titles[ii],
          {'ha': 'center', 'va': va},
          fontsize = fontsize,
        )
      
      xt = xRight + xMax*barWidth/2
      if titleTop:
        yt = titleGap*plotHeight +(rightWidths[rightLabel]['bottom'] + rightWidths[rightLabel]['right'])
        va = 'bottom'
      else:
        yt = -yscale*titleGap*plotHeight
        va = 'top'
                  
      plt.text(xt, yt, titles[ii+1],
        {'ha': 'center', 'va': va},
        fontsize = fontsize,
      )

    # Plot strips
    for leftLabel in leftLabels:
        for rightLabel in rightLabels:
            
            if len(dataFrame[(dataFrame.left == leftLabel) & (dataFrame.right == rightLabel)]) > 0:
                Ndiv = 10
                Narr = 25
                # Create array of y values for each strip, half at left value,
                # half at right, convolve
                ys_d = np.array(Narr * [leftWidths[leftLabel]['bottom']] + Narr * [rightWidths[rightLabel]['bottom']])
                ys_d = np.convolve(ys_d, 1/Ndiv * np.ones(Ndiv), mode='valid')
                ys_d = np.convolve(ys_d, 1/Ndiv * np.ones(Ndiv), mode='valid')
                ys_u = np.array(Narr * [leftWidths[leftLabel]['bottom'] + ns_l[leftLabel][rightLabel]] + Narr * [rightWidths[rightLabel]['bottom'] + ns_r[leftLabel][rightLabel]])
                ys_u = np.convolve(ys_u, 1/Ndiv * np.ones(Ndiv), mode='valid')
                ys_u = np.convolve(ys_u, 1/Ndiv * np.ones(Ndiv), mode='valid')

                # Update bottom edges at each label so next strip starts at the right place
                leftWidths[leftLabel]['bottom'] += ns_l[leftLabel][rightLabel]
                rightWidths[rightLabel]['bottom'] += ns_r[leftLabel][rightLabel]
                
                xx = np.linspace(xLeft, xRight, len(ys_d))
                cc = combineColours(colorDict[leftLabel],colorDict[rightLabel],len(ys_d))
                
                for jj in range(len(ys_d)-1):
                  plt.fill_between(
                    xx[[jj,jj+1]], 
                    ys_d[[jj,jj+1]], 
                    ys_u[[jj,jj+1]],
                    color=cc[:,jj],
                    alpha=alpha,
                    lw=0,
                    edgecolor="none",
                    snap=True,
                  )

