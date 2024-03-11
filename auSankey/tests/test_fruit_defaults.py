import matplotlib.pyplot as plt
import auSankey as sky
from .test_fruit_setup import TestFruit

class TestFruitDefault(TestFruit):

    def test_fruits_default(self):

        plt.figure(dpi=150)
        sky.sankey(self.data)

    def test_fruits_sorting(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, sorting=1)
        
        plt.figure(dpi=150)
        sky.sankey(self.data, sorting=-1)

    def test_fruits_colormap(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, colormap="jet")

    def test_fruits_colordict(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, colorDict=self.colorDict)
        
    def test_fruits_titles(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, titles=["Summer", "Winter"])
    
    def test_fruits_valign(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, valign="top")
        
        plt.figure(dpi=150)
        sky.sankey(self.data, valign="center")
        
        plt.figure(dpi=150)
        sky.sankey(self.data, valign="bottom")

