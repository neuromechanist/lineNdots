# lineNdots

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction
**lineNdots** is a Python toolbox to create beautiful and meaningful plots, especially for longitudinal data (e.g., repeated measures experiments with pre and post or multiple conditions). It is inspired by the [RainCloud](https://github.com/njudd/ggrain) is an inspiration for having beautiful and meaningful plots, especially for longitudinal data (e.g., repeated measures experiments with pre and post or multiple conditions). However, there are some drawbacks especially for the Python version of the RainCloud plots that made me work on lineNdots:

1. The longitudinal aspect is not complete in the Python version of RainCloud. The R version nicely provide hairline plots between individual data point for the longitudinal data. However, the Python version lacks this feature.
2. KDEs and box plots are not always the best visualization. While KDEs are very nice and informative when there is a good amount of data points (>30), for smaller distributions, which is often the case in biomechanics, they can be misleading. Further, box plots mainly reflect the median and IQRs and the range of the data, whereas the statistical tests performed on the data are usually comparing the mean and standard deviation. This creates a discrepancy between the statistics and the presented data. The problem sis more pronounced with smaller populations as there would be possibly bigger difference between the median and mean.

lineNdots tries to address these two main issues. Further, I have tried to work mainly within the boundaries of the Seaborn toolbox and manipulated its variables to achieve my plots. So, as long as you can pass the data as a Seaborn stripplot, you should also be able to plot lineNdots, without additional arguments. However, you can control lineNdots and override its defaults with additional arguments. Here are the synopsis the features of the lineNdots toolbox:

1. Longitudinal data are connected by individual hairlines, unless set to False.
2. KDEs are removed. Box plots are replaced by a central dot and line, which by default indicate average and STE.
3. The values ventral dot and the lines can be changed to median and IQR or any other quantity. Just pass the function.
4. Enjoy using Seaborn's awesome color pallets and features. lineNdots just moves Seaborn elements around.

## Installation
Use PyPi or pull from this repo and do an installation:

```shell
pip install lineNdots
```

## How to use
Similar to a stripplot, plot using lineNdots:

```Python
import lineNdots as lnd

lnd.lnd(data=box_data, y='average CI', x='age', ax=ax[i], palette='Set2', adtnl_space=0.2,
        mean_size=0.3, size=10, lw=4)
```

## Development path
Upon completion!, lineNdots should be able to function similar to ggrain, but in Python. To achieve this goal, we need smaller steps:

- [ ] control of the `stripplot` on left or right, as well as flipping them with longitudinal data
  - `rain.side: Which side to display the rainclouds: 'l' for left, 'r' for right and 'f' for flanking`
- [ ] It is all about the **hairlines**.
- [ ] make center dot and lines customizable.
- [ ] create unit tests
- [ ] afford complex plots, like the following ggrain feature set: `id.long.var, cov, y-jittering`
- [ ] create documentation
- [ ] release beta and get feedback
