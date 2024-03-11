
import pysankey as sky
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame([
  ("a",1.0,"ab",2.0,"a",1.0),
  ("a",1.0,"ba",0.8,"ba",0.4),
  ("c",1.5,"cd",0.5,"d",2.0),
  ("b",0.5,"ba",0.8,"ba",0.4),
  ("b",0.5,"ab",0.8,"a",1.0),
  ("d",2.0,"cd",0.4,"d",1.0),
  ("e",1.0,"e",1.0,"e",3.0),
])

plt.figure()
sky.sankey(
  data,
  sorting    = -1,
  titles    = ["Stage 1","Stage 2","Stage 3"],
  valign    = "center",
)
plt.show()

