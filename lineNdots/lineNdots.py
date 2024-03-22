
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def lnd(
    data, y, hue, x=None,
    agg_function=np.mean, var_function=np.std,
    palette=None, ax=None, colors=None, line=None, dots=None, flipped=None, 
    verbose=False, adtnl_space=0, intr_space=0, mean_size=0, size=0, lw=0, x_padding=0.1, legend=False
) -> plt.Axes:
    if ax is None:
        _, ax = plt.subplots(1, 1)
    if x is not None:
        ax = sns.stripplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
    else:
        ax = sns.stripplot(data=data, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
        ax.set_xticks(range(len(data[hue].unique())))
        ax.set_xticklabels(data[hue].unique())

    for i, art in enumerate(ax.collections):
        try:
            offsets = np.ma.getdata(art.get_offsets())
            agg = agg_function(offsets, axis=0)  # first number is x (agg position), second is y (agg value)
            # The line `varx = var_function(offsets, axis=0)` is calculating the
            # variability measure of the data points along the specified axis
            # (axis=0 in this case).
            varx = var_function(offsets, axis=0)  # varx is the variability measure
            if x is not None:
                if agg[0] < i // 2:
                    art.set_offsets(offsets - [adtnl_space, 0])
                    agg[0] = agg[0] + adtnl_space
                else:
                    art.set_offsets(offsets + [adtnl_space, 0])
                    agg[0] = agg[0] - adtnl_space
            else:
                art.set_offsets(offsets - [agg[0] - i + adtnl_space, 0])
                agg[0] = i + adtnl_space

            art.set_facecolor(palette[i % 2])
            ax.plot([agg[0], agg[0]], [agg[1] - varx[1], agg[1] + varx[1]],
                    color=art.get_facecolor()[0], lw=lw)
            ax.plot(agg[0], agg[1], markersize=mean_size, marker='o',
                    markeredgecolor=art.get_facecolor()[0], markerfacecolor='w', markeredgewidth=lw + 1)
        except Exception:
            if verbose:
                print('empty collection encountered')

    # Add horizontal padding
    ax.margins(x=x_padding)

    # add/remove legend
    if legend:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.get_legend().remove()

    return ax
