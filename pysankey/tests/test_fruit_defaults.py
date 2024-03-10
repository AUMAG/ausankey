import matplotlib.pyplot as plt
from pysankey import sankey as sky
from .test_fruit_setup import TestFruit

print(dir(sky))

class TestFruitDefault(TestFruit):

    def test_fruits_default(self):
        
        plt.figure(dpi=150)
        sky.sankey(self.data)
        plt.savefig("fruits_default.png")
