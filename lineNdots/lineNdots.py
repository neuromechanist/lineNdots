
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def lnd(
    data, y, hue, palette, ax, colors, line, dots, average, flipped, verbose, adtnl_space, intr_space, mean_size,
    size, lw, x=None
):
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
            average = offsets.mean(axis=0)  # first number is x (mean position), second is y (mean value)
            std = offsets.std(axis=0)
            if x is not None:
                if average[0] < i // 2:
                    art.set_offsets(offsets - [adtnl_space, 0])
                    average[0] = average[0] + adtnl_space
                else:
                    art.set_offsets(offsets + [adtnl_space, 0])
                    average[0] = average[0] - adtnl_space
            else:
                art.set_offsets(offsets - [average[0] - i + adtnl_space, 0])
                average[0] = i + adtnl_space

            # if colors is not None:
            # art.set_facecolor(colors[data[hue].unique()[i % 2]][i // 2])
            art.set_facecolor(palette[i % 2])
            ax.plot([average[0], average[0]], [average[1] - std[1], average[1] + std[1]],
                    color=art.get_facecolor()[0], lw=lw)
            ax.plot(average[0], average[1], markersize=mean_size, marker='o',
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
