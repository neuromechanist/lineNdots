import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def lnd(
    data, y, hue, x=None,
    agg_function=np.mean, var_function=np.std,
    palette=None, ax=None, colors=None,
    line=True, dots=True, dot_marker='o', flipped=False,
    verbose=False, adtnl_space=0, mean_size=0, size=0, lw=0, x_padding=0.1, legend=False,
    hairlines=False  # New parameter to control hairlines
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
                ax.plot([red[0], blue[0]], [red[1], blue[1]], color='gray', linestyle='--', linewidth=0.5)

    # Set the x-axis range to include all the data and adjust for horizontal padding
    ax.set_xlim(ax.get_xlim()[0] - mux * 0.1, ax.get_xlim()[1] + 0.2 - mux * 0.1)
    ax.margins(x=x_padding)

    # Add or remove legend
    if legend:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        legend = ax.get_legend()
        if legend:
            legend.remove()

    return ax
