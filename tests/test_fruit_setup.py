import pandas as pd
from .generic_test import GenericTest


class TestFruit(GenericTest):
    """ Setup sankey test with data in fruit.csv """

    def setUp(self):
        
        self.figure_name = "fruit"
        self.data = pd.read_csv(
            'tests/fruit.csv', sep=','
        )
        self.colorDict = {
            'apple': '#f71b1b',
            'blueberry': '#1b7ef7',
            'banana': '#f3f71b',
            'lime': '#12e23f',
            'orange': '#f78c1b'
        }

