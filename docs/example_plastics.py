
import matplotlib.pyplot as plt
import pandas as pd

import ausankey as sky

data = pd.DataFrame([
  (
   "Total",100*0.7,
   "Used Once",100*0.7,
   None,None,
   None,None,
  ),
  (
   "Total",100*0.3,
   "Still Used",100*0.3,
   "Still Used",100*0.3,
   "Still Used",100*0.3,
  ),
  (
   None,None,
   "Used Once",100*0.55,
   "Discarded",100*0.55,
   "Discarded",100*0.55,
  ),
  (
   None,None,
   "Used Once",100*0.09,
   "Incinerated",100*0.09,
   "Incinerated",100*0.09,
  ),
  (
   None,None,
   "Used Once",100*0.06,
   "Recycled",100*0.06,
   None,None,
  ),
  (
   None,None,
   None,None,
   "Recycled",100*0.04,
   "Discarded",100*0.04,
  ),
  (
   None,None,
   None,None,
   "Recycled",100*0.01,
   "Incinerated",100*0.01,
  ),
  (
   None,None,
   None,None,
   "Recycled",100*0.01,
   "Still Used",100*0.01,
  ),
])

plt.figure(dpi=600,figsize=(10,10))


sky.sankey(
  data,
  node_lw=3,
  flow_lw=1.5,
  label_width = 0.1,
  label_gap   = 0.02,
  node_width  = 0.06,
  node_gap    = 0.08,
  node_alpha  = 1,
  node_edge = True,
  flow_alpha  = 0.4,
  flow_edge = True,
  title_gap  = 0.02,
  title_side = "both",
  title_loc  = "outer",
  frame_side = "both",
  frame_lw = 0,
  label_loc = ["top", "top", "top"],
  value_loc = ["right", "right", "right"],
  sort = "top",
  sort_dict = {"Still Used":999},
  label_duplicate = True,
 # label_font = {"color": "red", "rotation": 90},
  valign    = "top",
  value_gap = 0.03,
  value_font = {"color": [0, 0, 0], "fontweight": "bold"},
  label_font = {"color": [0, 0, 0], "fontweight": "bold"},
  colormap = "jet",
)


plt.show()
plt.savefig("example_plastics.png")
plt.close()


