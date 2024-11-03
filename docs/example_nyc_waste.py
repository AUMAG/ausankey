
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import ausankey as sky

data = pd.read_csv('nyc-trash.csv')

plt.figure(figsize=(15,18),dpi=600)
sky.sankey(data,
  colormap = "plasma",
  node_gap = 0.02,
  node_width = 0.3,
  sort = "bottom",
  sort_dict = {"Trash": 99999, "Non-divertible": 99999},
  valign = "bottom",
  node_lw = 0,
  label_gap = 0.03,
  label_loc = "center",
  label_values = True,
  label_dict = { 
      "Metal, Glass, Plastics": "Metal, Glass,\nPlastics" ,
      "Paper & Cardboard": "Paper and\nCardboard" ,
  }, 
  value_duplicate = False,
  value_loc = "both",
  value_thresh_val = 200,
  label_font = {
      "bbox": {
          "color": "white",
          "alpha": 0.5,
      }
  }
)

plt.show()
plt.savefig("example_nyc_waste.png")
plt.close()

