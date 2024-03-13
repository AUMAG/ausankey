
import auSankey as sky
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('tests/fruit.csv')
print(data)

plt.figure()
sky.sankey(data)
plt.show()
plt.savefig("doc/fruits_default.png")

data = pd.DataFrame([
    ("apple", 1, "apple", 0.5),
    ("banana", 2, "banana", 3),
    ("lime", 0.5, "lime", 0.2),
    ("blueberry", 0.2, "blueberry", 1),
    ("orange", 1.5, "orange", 1.5),
])

plt.figure()
sky.sankey(data,colormap="jet")
plt.show()
plt.savefig("doc/fruits_jet.png")

colorDict = {
    'apple':     '#f71b1b',
    'blueberry': '#1b7ef7',
    'banana':    '#f3f71b',
    'lime':      '#12e23f',
    'orange':    '#f78c1b'
}

plt.figure()
sky.sankey(data,colorDict=colorDict)
plt.show()
plt.savefig("doc/fruits_colordict.png")

labelDict = {
    'apple':     'Apple',
    'blueberry': "B'berry",
    'banana':    'Banana',
    'lime':      'Lime',
    'orange':    'Orange'
}

plt.figure()
sky.sankey(data,labelDict=labelDict)
plt.show()
plt.savefig("doc/fruits_labeldict.png")

plt.figure()
sky.sankey(data,alpha=0.3)
plt.show()
plt.savefig("doc/fruits_alpha.png")

plt.figure()
sky.sankey(data,sorting=1)
plt.show()
plt.savefig("doc/fruits_sort_p1.png")

plt.figure()
sky.sankey(data,sorting=-1)
plt.show()
plt.savefig("doc/fruits_sort_n1.png")

plt.figure()
sky.sankey(data,titles=["Summer","Winter"])
plt.show()
plt.savefig("doc/fruits_titles.png")

plt.figure()
sky.sankey(data,
    titles = ["Summer","Winter"],
    titleSide = "bottom",
)
plt.show()
plt.savefig("doc/fruits_titles_bottom.png")

plt.figure()
sky.sankey(data,valign="center")
plt.show()
plt.savefig("doc/fruits_valign.png")

plt.figure()
sky.sankey(data,frameSide="both")
plt.show()
plt.savefig("doc/fruits_frame.png")

plt.figure()
sky.sankey( data,
            titles=["Summer","Winter"],
            titleSide = "both",
            frameSide = "both",
            sorting   = -1,
            valign    = "center",
            # spacing parameters:
            barGap     = 0.01 ,
            barWidth   = 0.1 ,
            frameGap   = 0.2 ,
            labelWidth = 0.3 ,
            labelGap   = 0.02,
            titleGap   = 0.1 ,
          )
plt.show()
plt.savefig("doc/fruits_spacing.png")

data = pd.DataFrame([
  ("a",1.0,"ab",2.0),
  ("a",1.0,"ba",0.8),
  ("c",1.5,"cd",0.5),
  ("b",0.5,"ba",0.8),
  ("b",0.5,"ab",0.8),
  ("d",2.0,"cd",0.4),
  ("e",1.0,"e",1.0),
])

plt.figure()
sky.sankey(
  data,
  sorting = -1,
  colormap = "jet",
  aspect=0.5
)
plt.savefig("doc/frame2_sort_n1.png")


colorDict =  {
   'a':'#f71b1b',
   'b':'#1b7ef7',
  'ab':'#8821aa',
  'ba':'#6016aa',
  'cd':'#c1e849',
   'c':'#f3f71b',
   'd':'#12e23f',
   'e':'#f78c1b',
 }

data = pd.DataFrame([
  ("a",1.0,"ab",2.0,"a",1.0),
  ("a",1.0,"ba",0.8,"ba",0.4),
  ("c",1.5,"cd",0.5,"d",2.0),
  ("b",0.5,"ba",0.8,"ba",0.4),
  ("b",0.5,"ab",0.8,"a",1.0),
  ("d",2.0,"cd",0.4,"d",1.0),
  ("e",1.0,"e",1.0,"e",3.0),
])

plt.figure(dpi=600)

sky.sankey(
  data,
  sorting    = -1,
  colorDict  = colorDict,
  labelWidth = 0.1,
  labelGap   = 0.02,
  barWidth   = 0.05,
  barGap     = 0.02,
  alpha      = 0.3,
  titles    = ["Stage 1","Stage 2","Stage 3"],
  titleGap  = 0.05,
  titleSide = "both",
  frameSide = "both",
  frameGap  = 0.1,
  valign    = "top",
)

plt.savefig("doc/frame3_many.png")


