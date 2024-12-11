import pandas as pd
import trplots as trp
from plot_settings import (
    BOX_PLOT_SETTINGS,
    MEAN_PLOT_SETTINGS,
    OUTLIER_PLOT_SETTINGS,
    SWARM_PLOT_SETTINGS,
    LINE_PLOT_SETTINGS,
)


def gen_box_graph(
    ax,
    data,
    sample_filter,
    is_add_jitter,
    brackets,
    bracket_base_y,
    bracket_h_ratio=0.02,
    bracket_hspace_ratio=0.1,
    bracket_mark_fs=10,
    x_col_id=0,
    y_col_id=3,
    hue_col_id=2,
):
    """
    Args:
        ax: matplotlib.axes.Axes
            boxplotを描画するAxes
        data: pd.DataFrame
            描画するデータ (列名はx_col_id, y_col_id, hue_col_idで指定)
            schemeta_splitterで定義されるワイド形式を推奨
        sample_filter:
            描画するデータのサンプル名のリスト(hue_col_idで指定される列の値)
            空の場合は全データを使用
        is_add_jitter:
            boxplotにjitterを追加するかどうか
        brackets:
            ブラケットのリスト, ブラケットは[[[sample1, group1], [sample2, group2], mark], ...]の形式
            すべてstr型
            sample1, sample2: x軸の値に対応
            group1, group2: hue軸の値に対応
        bracket_base_y:
            ブラケットを描画する最低y座標
        bracket_h_ratio:
            ブラケットの高さのグラフエリアに対する比率
        bracket_hspace_ratio:
            ブラケット間の間隔のグラフエリアに対する比率
        bracket_mark_fs:
            ブラケットのマークのフォントサイズ
        x_col_id:
            dataの列名のインデックス (x軸)
        y_col_id:
            dataの列名のインデックス (y軸)
        hue_col_id:
            dataの列名のインデックス (hue)

    Returns:
        ax: matplotlib.axes.Axes
            boxplotが描画されたAxes
    """
    box_kwargs = BOX_PLOT_SETTINGS.copy()
    mean_kwargs = MEAN_PLOT_SETTINGS.copy()
    outlier_kwargs = OUTLIER_PLOT_SETTINGS.copy()
    swarm_kwargs = SWARM_PLOT_SETTINGS.copy()

    # dataの列名を取得
    x = data.columns[x_col_id]
    y = data.columns[y_col_id]
    hue = data.columns[hue_col_id]

    # dataからsample_filterに従ってデータを抽出(xに一致するデータを抽出)
    if len(sample_filter) > 0:
        data = data[data[x].isin(sample_filter)]
        # dataをsample_filterの順に並び替える
        data[x] = pd.Categorical(data[x], categories=sample_filter, ordered=True)
    else:
        # sample_filterが空の場合は全データを使用 (xをすべて""に書き換える)
        data[x] = ""

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
        h_ratio=bracket_h_ratio,
        hspace_ratio=bracket_hspace_ratio,
        fs=bracket_mark_fs,
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
