# %% Initialize
from lineNdots import lnd
import numpy as np
import pandas as pd
import seaborn as sns

# %% Create data
np.random.seed(0)

# Create a random dataset
data = pd.DataFrame({
    'x': np.random.choice(['A', 'B', 'C'], 20),
    'y': np.random.normal(0, 1, 20),
    'hue': np.random.choice(['red', 'blue'], 20)
})

# Create a palette
palette = sns.color_palette("pastel", 2)

# %% Plot without Line and Dots
# Create a stripplot
ax = sns.stripplot(data=data, x='x', y='y', hue='hue', palette=palette, dodge=True, size=10)

# Set the x-ticks
ax.set_xticks(range(len(data['x'].unique())))
ax.set_xticklabels(data['x'].unique())

# Add Line and dots without using lnd
for i, art in enumerate(ax.collections):
    try:
        offsets = np.ma.getdata(art.get_offsets())
        average = offsets.mean(axis=0)  # first number is x (mean position), second is y (mean value)
        std = offsets.std(axis=0)
        if average[0] < i // 2:
            art.set_offsets(offsets - [0.1, 0])
            average[0] = average[0] + 0.1
        else:
            art.set_offsets(offsets + [0.1, 0])
            average[0] = average[0] - 0.1
        art.set_facecolor(palette[i % 2])
        ax.plot([average[0], average[0]], [average[1] - std[1], average[1] + std[1]],
                color=art.get_facecolor()[0], lw=2)
        ax.plot(average[0], average[1], markersize=10, marker='o',
                markeredgecolor=art.get_facecolor()[0], markerfacecolor='w', markeredgewidth=2)
    except Exception:
        print('empty collection encountered')

# %% Plot with lnd
lnd(
    data, 'y', 'hue', 'x', palette=None, agg_function=np.median, var_function=np.std,
    ax=None, colors=list(palette), line=True, dots=True, flipped=False,
    verbose=False, adtnl_space=0.1, mean_size=20, size=10, lw=2)
