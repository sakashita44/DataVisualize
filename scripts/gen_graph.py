import trplots as trp
from plot_settings import (
    BOX_PLOT_SETTINGS,
    MEAN_PLOT_SETTINGS,
    OUTLIER_PLOT_SETTINGS,
    SWARM_PLOT_SETTINGS,
    LINE_PLOT_SETTINGS,
)


def gen_box_graph(ax):
    """ """
    box_kwargs = BOX_PLOT_SETTINGS.copy()
    mean_kwargs = MEAN_PLOT_SETTINGS.copy()
    outlier_kwargs = OUTLIER_PLOT_SETTINGS.copy()
    swarm_kwargs = SWARM_PLOT_SETTINGS.copy()

    box_trp = trp.TrendPlots(ax)
    box_trp.add_box_mean_plot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        is_add_jitter=is_add_jitter,
        jitter_setting=swarm_kwargs,
        mean_setting=mean_kwargs,
        flierprops=outlier_kwargs,
        **box_kwargs,
    )
    box_trp.add_brackets(
        brackets=brackets,
        bracket_base_y=bracket_base_y,
        h_ratio=h_ratio,
        hspace_ratio=hspace_ratio,
        fs=fs,
    )

    return box_trp.ax


def gen_line_mean_sd_graph(ax):
    """ """
    line_kwargs = LINE_PLOT_SETTINGS.copy()

    line_trp = trp.TrendPlots(ax)
    line_trp.add_line_mean_sd_plot(data=data, order=order, **line_kwargs)

    return line_trp.ax


def gen_individual_line_graph(ax):
    """ """
    line_kwargs = LINE_PLOT_SETTINGS.copy()

    line_trp = trp.TrendPlots(ax)
    line_trp.add_line_group_coloring_plot(data=data, order=order, **line_kwargs)

    return line_trp.ax
