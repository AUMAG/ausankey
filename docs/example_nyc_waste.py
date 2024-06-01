
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import ausankey as sky

data = pd.read_csv('nyc-trash.csv')

plt.figure(figsize=(15,12),dpi=600)
sky.sankey(data,
  colormap = "plasma",
  node_gap = 0.04,
  node_width = 0.4,
  sort = "top",
  sort_dict = {"Trash": 99999, "Non-divertible": 99999},
  valign = "top",
  node_lw = 0,
  label_gap = 0.03,
  label_loc = ["center","center","center"],
  value_loc = ["both","both","both"],
  value_thresh_val = 200,
  label_font = {
      "bbox": {
          "color": "white",
          "alpha": 0.5,
      }
  }
)
plt.show()

