import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import ausankey as sky

data = pd.read_csv('nyc-trash.csv')

plt.figure(figsize=(15,15),dpi=600)
sky.sankey(data,
  colormap = "nipy_spectral",
  node_gap = 0.07,
  node_width = 0.2,
  node_lw = 0,
  label_gap = 0.02,
  label_loc = ["top","top","top"],
  value_loc = ["both","both","both"],
  value_thresh_val = 200,
)
plt.show()
plt.savefig("example_nyc_waste.png")
plt.close()

