
import pysankey as sky
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv(
    'pysankey/tests/fruit.csv',
    sep=',',
)
print(data)

plt.figure()
sky.sankey(data)
plt.show()

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
  
plt.show()

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

plt.show()


