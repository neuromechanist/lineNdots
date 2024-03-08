import unittest
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .. import lnd


class TestCombinedLnd(unittest.TestCase):
    def setUp(self):
        # Set the seed for reproducibility
        np.random.seed(0)

        # Create a random dataset
        self.data = pd.DataFrame({
            'x': np.random.choice(['A', 'B', 'C'], 100),
            'y': np.random.normal(0, 1, 100),
            'hue': np.random.choice(['red', 'blue'], 100)
        })

        # Create a palette
        self.palette = sns.color_palette("hls", 8)

    def test_lnd_with_x(self):
        # Create a figure and axes
        fig, ax = plt.subplots()

        # Test the function with x
        try:
            lnd(
                self.data, 'y', 'hue', self.palette, ax, None, None, None, None, None, False, 0.1, 0.1, 10, 5, 1, 'x'
            )
        except Exception as e:
            self.fail(f"lnd raised exception with x: {e}")

    def test_lnd_without_x(self):
        # Create a figure and axes
        fig, ax = plt.subplots()

        # Test the function without x
        try:
            lnd(
                self.data, 'y', 'hue', self.palette, ax, None, None, None, None, None, False, 0.1, 0.1, 10, 5, 1
            )
        except Exception as e:
            self.fail(f"lnd raised exception without x: {e}")


if __name__ == '__main__':
    unittest.main()
