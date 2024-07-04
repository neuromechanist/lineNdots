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
    """
    Plot line and dots for grouped data.

    Parameters:
    -----------
    data : DataFrame
        The input data.
    y : str
        The name of the column to be plotted on the y-axis.
    hue : str
        The name of the column used for grouping the data.
    x : str, optional
        The name of the column to be plotted on the x-axis. If not provided, the x-axis will be categorical.
    agg_function : function, optional
        The function used to aggregate the data points within each group. Default is np.mean.
    var_function : function, optional
        The function used to calculate the variability measure of the data points within each group. Default is np.std.
    palette : str or list, optional
        The color palette to be used for the groups. If not provided, a default palette will be used.
    ax : Axes object, optional
        The matplotlib Axes object to draw the plot on. If not provided, a new figure and Axes object will be created.
    colors : list, optional
        Deprecated argument. Use palette instead.
    line : bool, optional
        Whether to plot the line connecting the aggregated points. Default is True.
    dots : bool, optional
        Whether to plot the individual data points as dots. Default is True.
    dot_marker : str, optional
        The marker style for the dots. Default is 'o'.
    flipped : bool, optional
        Whether to flip the x-axis. Default is False.
    verbose : bool, optional
        Whether to display verbose warnings. Default is False.
    adtnl_space : float, optional
        Additional space between the aggregated points. Default is 0.1.
    mean_size : float, optional
        The size of the marker for the aggregated points. Default is 20.
    size : float, optional
        The size of the marker for the individual data points. Default is 10.
    lw : float, optional
        The linewidth for the line and marker edges. Default is 2.
    padding : float, optional
        The padding factor for adjusting the x and y axis limits. Default is 0.1.
    legend : bool, optional
        Whether to display the legend. Default is False.
    hairlines : bool, optional
        Whether to draw hairlines for paired comparisons. Default is False.
    hairline_color : str, optional
        The color of the hairlines. Default is 'gray'.
    hairline_style : str, optional
        The line style of the hairlines. Default is '--'.
    hairline_width : float, optional
        The linewidth of the hairlines. Default is 0.5.

    Returns:
    --------
    ax : Axes object
        The matplotlib Axes object containing the plot.

    Raises:
    -------
    ValueError
        If both colors and palette are provided.

    Notes:
    ------
    - Only one of the color and palette can be provided.
    - If verbose is False, warnings will be suppressed.
    - The x-axis range will be adjusted to include all the data and adjust for horizontal padding.
    - The y-axis range will be adjusted to include all the data and adjust for vertical padding.
    - If legend is True, the legend will be displayed on the right side of the plot.
    - If legend is False, the legend will be removed from the plot.
    - If hairlines is True, hairlines will be drawn for paired comparisons.
    """

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
    if hairlines:
        _drawHairlines(data, x, ax, hairline_color, hairline_style, hairline_width, hue_values, scatter_offsets)

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


def _drawHairlines(data, x, ax, hairline_color, hairline_style, hairline_width, hue_values, scatter_offsets):
    """
    Draw hairlines between scatter plot points based on hue values.

    Parameters:
    data (pandas.DataFrame): The input data.
    x (str): The column name representing the x-axis values.
    ax (matplotlib.axes.Axes): The matplotlib axes object to draw on.
    hairline_color (str): The color of the hairlines.
    hairline_style (str): The style of the hairlines.
    hairline_width (float): The width of the hairlines.
    hue_values (list): The list of hue values.
    scatter_offsets (dict): The dictionary of scatter offsets.

    Returns:
    None
    """
    if len(hue_values) == 2:
        for category in data[x].unique():
            pre_offsets = np.vstack([offset for offset in scatter_offsets[hue_values[0]]])
            post_offsets = np.vstack([offset for offset in scatter_offsets[hue_values[1]]])
            for pre, post in zip(pre_offsets, post_offsets):
                ax.plot([pre[0], post[0]], [pre[1], post[1]],
                        color=hairline_color, linestyle=hairline_style, lw=hairline_width)
