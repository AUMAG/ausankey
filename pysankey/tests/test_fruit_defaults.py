
import matplotlib as plt
from pysankey import sankey
from .test_fruit import TestFruit


class TestFruitDefault(TestFruit):

    def test_fruits_default(self):
        
        plt.figure(dpi=150)
        sankey(self.data)
        plt.savefig("fruits_default.png")
