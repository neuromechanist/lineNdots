
import seaborn as sns
import numpy.ma as ma

def lnd(
    data, y, hue, palette, ax, colors, line, dots, average, flipped, verbose, adtnl_space, intr_space, mean_size,
    size, lw, x=None
):
    if x is not None:
        ax = sns.stripplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
    else:
        ax = sns.stripplot(data=data, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
        ax.set_xticks(range(len(data[hue].unique())))
        ax.set_xticklabels(data[hue].unique())

    for i, art in enumerate(ax.collections):
        try:
            offsets = ma.getdata(art.get_offsets())
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

            if colors is not None:
                art.set_facecolor(colors[data[hue].unique()[i % 2]][i // 2])
            ax.plot([average[0], average[0]], [average[1] - std[1], average[1] + std[1]],
                    color=art.get_facecolor()[0], lw=lw)
            ax.plot(average[0], average[1], markersize=mean_size * 100, marker='o',
                    markeredgecolor=art.get_facecolor()[0], markerfacecolor='w', markeredgewidth=lw + 1)
        except Exception:
            if verbose:
                print('empty collection encountered')

    if x is None:
        ax.margins(x=0.3)

    return ax
