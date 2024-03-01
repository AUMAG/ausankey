
import pysankey as sky
import matplotlib.pyplot as plt
import pandas as pd

colorDict =  {'a':'#f71b1b','b':'#1b7ef7','c':'#f3f71b','d':'#12e23f','orange':'#f78c1b'}

data = pd.DataFrame([
  ("a",1.0,"a",2.0),
  ("a",1.0,"b",0.8),
  ("c",1.5,"c",0.5),
  ("b",0.5,"b",0.8),
  ("b",0.5,"a",0.8),
  ("d",2.0,"c",0.4),
  ])

sky.sankey(
  data,
  sorting = -1,
  colorDict = colorDict,
  )
  
#plt.gcf().set_size_inches(6,6)
# plt.savefig('fruits.png',bbox_inches='tight',dpi=150)

plt.show()

