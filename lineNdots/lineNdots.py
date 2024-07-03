import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def lnd(
    data, y, hue, x=None,
    agg_function=np.mean, var_function=np.std,
    palette=None, ax=None, colors=None,
    line=True, dots=True, dot_marker='o', flipped=False,
    verbose=False, adtnl_space=0.1, mean_size=20, size=10, lw=2, padding=0.1, legend=False,
    hairlines=False, hairline_color='gray', hairline_style='--', hairline_width=0.5
) -> plt.Axes:
    # Only one of the color and palette can be provided
    if colors is not None and palette is not None:
        raise ValueError('Only one of the color and palette can be provided')
    if colors is not None:
        palette = colors
    if verbose is False:  # if verbose is False, suppress warnings
        import warnings
        warnings.filterwarnings("ignore")
    if ax is None:
        _, ax = plt.subplots(1, 1)
    if x is not None:
        ax = sns.stripplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
    else:
        ax = sns.stripplot(data=data, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
        ax.set_xticks(range(len(data[hue].unique())))
        ax.set_xticklabels(data[hue].unique())

    # Do not advance if line and dots are False
    if not line and not dots:
        return ax

    hue_values = data[hue].unique()
    scatter_offsets = {hue_val: [] for hue_val in hue_values}

    for i, art in enumerate(ax.collections):
        try:
            offsets = np.ma.getdata(art.get_offsets())
            agg = agg_function(offsets, axis=0)  # first number is x (agg position), second is y (agg value)
            varx = var_function(offsets, axis=0)  # varx is the variability measure

            mux = -1 if flipped else 1  # mux is the multiplier for flipped
            if x is not None:
                if agg[0] < i // 2:
                    art.set_offsets(offsets - [adtnl_space * mux, 0])
                    agg[0] = agg[0] + adtnl_space * mux
                else:
                    art.set_offsets(offsets + [adtnl_space * mux, 0])
                    agg[0] = agg[0] - adtnl_space * mux
            else:
                art.set_offsets(offsets - [agg[0] - i + adtnl_space * mux, 0])
                agg[0] = i + adtnl_space * mux

            scatter_offsets[hue_values[i % len(hue_values)]].append(art.get_offsets())

            art.set_facecolor(palette[i % len(palette)])
            if line:
                ax.plot([agg[0], agg[0]], [agg[1] - varx[1], agg[1] + varx[1]],
                        color=art.get_facecolor()[0], lw=lw)
            if dots:
                ax.plot(agg[0], agg[1], markersize=mean_size, marker=dot_marker,
                        markeredgecolor=art.get_facecolor()[0], markerfacecolor='w', markeredgewidth=lw + 1)
        except Exception as e:
            if verbose:
                print(f'Error processing collection: {e}')

    # Draw hairlines for paired comparisons
    if hairlines and len(hue_values) == 2:
        for category in data[x].unique():
            red_offsets = np.vstack([offset for offset in scatter_offsets[hue_values[0]]])
            blue_offsets = np.vstack([offset for offset in scatter_offsets[hue_values[1]]])
            for red, blue in zip(red_offsets, blue_offsets):
                ax.plot([red[0], blue[0]], [red[1], blue[1]],
                        color=hairline_color, linestyle=hairline_style, lw=hairline_width)

    # Set the x-axis range to include all the data and adjust for horizontal padding
# Adjust x and y limits to center the figure
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    x_range = x_max - x_min
    y_range = y_max - y_min
    ax.set_xlim(x_min - padding * x_range, x_max + padding * x_range)
    ax.set_ylim(y_min - padding * y_range, y_max + padding * y_range)

    # Add or remove legend
    if legend:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        legend = ax.get_legend()
        if legend:
            legend.remove()

    return ax
