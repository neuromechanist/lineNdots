
import seaborn as sns


def lnd(
    data, x: str = None, y: str = None, hue: str = None, palette=None, ax=None, colors=None,
    line: bool = True, dots: bool = True, average: bool = True, flipped: bool = False, verbose: bool = False,
    adtnl_space: float = 0.10, intr_space: float = 0.20, mean_size: float = 0.10, size=5, lw: int = 2
):
    if x is None:
        _onesample_lnd(data, y, hue, palette, ax, colors, line, dots, average, flipped, verbose, adtnl_space,
                       intr_space, mean_size, size, lw)
    else:
        _hue_lnd(data, x, y, hue, palette, ax, colors, line, dots, average, flipped, verbose, adtnl_space,
                 intr_space, mean_size, size, lw)


def _hue_lnd(
    data, x, y, hue, palette, ax, colors, line, dots, average, flipped, verbose, adtnl_space, intr_space, mean_size,
    size, lw
):
    ax = sns.stripplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
    for i, art in enumerate(ax.collections):
        try:
            offsets = art.get_offsets()
            average = offsets.mean(axis=0)  # first number is x (mean position), second is y (mean value)
            std = offsets.std(axis=0)
            if average[0] < i // 2:
                art.set_offsets(offsets - [adtnl_space, 0])
                average[0] = average[0] + adtnl_space
            else:
                art.set_offsets(offsets + [adtnl_space, 0])
                average[0] = average[0] - adtnl_space
            if colors is not None:
                art.set_facecolor(colors[data[hue].unique()[i % 2]][i // 2])
            ax.plot([average[0], average[0]], [average[1] - std[1], average[1] + std[1]],
                    color=art.get_facecolor()[0], lw=lw)
            ax.plot(average[0], average[1], markersize=mean_size * 100, marker='o',
                    markeredgecolor=art.get_facecolor()[0], markerfacecolor='w', markeredgewidth=lw + 1)
        except IndexError:
            if verbose:
                 print('empty collection encountered')


def _onesample_lnd(
    data, y, hue, palette, ax, colors, line, dots, average, flipped, verbose, adtnl_space, intr_space, mean_size,
    size, lw
):
    ax = sns.stripplot(data=data, y=y, hue=hue, palette=palette, ax=ax, dodge=True, size=size)
    for i, art in enumerate(ax.collections):
        try:
            offsets = art.get_offsets()
            average = offsets.mean(axis=0)  # first number is x (mean position), second is y (mean value)
            std = offsets.std(axis=0)
            art.set_offsets(offsets - [average[0] - i + adtnl_space, 0])
            average[0] = i + adtnl_space
            ax.plot([average[0], average[0]], [average[1] - std[1], average[1] + std[1]],
                    color=art.get_facecolor()[0], lw=lw)
            ax.plot(average[0], average[1], markersize=mean_size * 100, marker='o',
                    markeredgecolor=art.get_facecolor()[0], markerfacecolor='w', markeredgewidth=lw + 1)
            ax.margins(x=0.3)
        except IndexError:
            if verbose:
                print('empty collection encountered')

    ax.set_xticks(range(len(data[hue].unique())))
    ax.set_xticklabels(data[hue].unique())
