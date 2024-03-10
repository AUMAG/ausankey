import matplotlib.pyplot as plt
import pysankey as sky
from .test_fruit_setup import TestFruit

class TestFruitDefault(TestFruit):

    def test_fruits_default(self):

        plt.figure(dpi=150)
        sky.sankey(self.data)
        plt.savefig("fruits_default.png")

    def test_fruits_sorting(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, sorting=1)
        plt.savefig("fruits_sorting_1.png")
        
        plt.figure(dpi=150)
        sky.sankey(self.data, sorting=-1)
        plt.savefig("fruits_sorting_2.png")

    def test_fruits_colormap(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, colormap="jet")
        plt.savefig("fruits_colormap_jet.png")

    def test_fruits_colordict(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, colorDict=self.colorDict)
        
    def test_fruits_titles(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data, titles=["Summer", "Winter"])
