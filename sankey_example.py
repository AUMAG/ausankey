
import pysankey as sky
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame([
  ("a",1.0,"ab",2.0),
  ("a",1.0,"ba",0.8),
  ("c",1.5,"cd",0.5),
  ("b",0.5,"ba",0.8),
  ("b",0.5,"ab",0.8),
  ("d",2.0,"cd",0.4),
  ("e",1.0,"e",1.0),
])

sky.sankey(
  data,
  sorting = -1,
  colormap = "jet",
  aspect=0.5
)
  
#plt.gcf().set_size_inches(6,6)
# plt.savefig('fruits.png',bbox_inches='tight',dpi=150)

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
  ("e",1.0,"e",1.0,"e",1.0),
])

sky.sankey(
  data,
  sorting = -1,
  colorDict = colorDict,
  labelWidth = 0.2,
  barWidth = 0.05,
  barGap = 0.02,
  alpha=0.3,
  titles = ["Line 1","Line 2","Line 3"],
  titleGap = 0.025,
  titleTop = False,
)

#plt.gcf().set_size_inches(6,6)
#plt.savefig('fruits.pdf',bbox_inches='tight')

plt.show()


