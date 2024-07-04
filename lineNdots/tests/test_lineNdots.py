
import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lineNdots.lineNdots import lnd

class TestLineNdots(unittest.TestCase):
    def setUp(self):
        # Create a sample dataframe
        np.random.seed(0)
        self.data = pd.DataFrame({
            'x': np.tile(np.arange(1, 6), 3),
            'y': np.random.randn(15),
            'hue': np.repeat(['A', 'B', 'C'], 5)
        })

    def test_lnd_basic(self):
        # Test if lnd runs without errors
        try:
            ax = lnd(self.data, y='y', hue='hue', x='x')
            self.assertIsInstance(ax, plt.Axes)
        except Exception as e:
            self.fail(f"lnd raised an exception {e}")

    def test_lnd_no_x(self):
        # Test if lnd runs without the x parameter
        try:
            ax = lnd(self.data, y='y', hue='hue')
            self.assertIsInstance(ax, plt.Axes)
        except Exception as e:
            self.fail(f"lnd raised an exception {e}")

    def test_lnd_with_line_and_dots(self):
        # Test if lnd runs with both line and dots
        try:
            ax = lnd(self.data, y='y', hue='hue', x='x', line=True, dots=True)
            self.assertIsInstance(ax, plt.Axes)
        except Exception as e:
            self.fail(f"lnd raised an exception {e}")

    def test_lnd_with_different_agg_function(self):
        # Test if lnd runs with a different aggregation function
        try:
            ax = lnd(self.data, y='y', hue='hue', x='x', agg_function=np.median)
            self.assertIsInstance(ax, plt.Axes)
        except Exception as e:
            self.fail(f"lnd raised an exception {e}")

    def test_lnd_with_hairlines(self):
        # Test if lnd runs with hairlines
        try:
            ax = lnd(self.data, y='y', hue='hue', x='x', hairlines=True)
            self.assertIsInstance(ax, plt.Axes)
        except Exception as e:
            self.fail(f"lnd raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
