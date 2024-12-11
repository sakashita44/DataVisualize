from random import sample
import pandas as pd
import trplots as trp

from data_processing import convert_data_to_lineplot
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
    is_add_jitter,
    brackets,
    bracket_base_y,
    bracket_h_ratio=0.02,
    bracket_hspace_ratio=0.1,
    bracket_mark_fs=10,
    x_col_id=0,
    y_col_id=3,
    hue_col_id=2,
    hue_order=None,
    sample_filter=[],
):
    """
    Args:
        ax: matplotlib.axes.Axes
            boxplotを描画するAxes
        data: pd.DataFrame
            描画するデータ (列名はx_col_id, y_col_id, hue_col_idで指定)
            schemeta_splitterで定義されるワイド形式にのみ対応 (この場合x_col_id, y_col_id, hue_col_idは0, 3, 2で固定)
        sample_filter:
            描画するデータのサンプル名のリスト(hue_col_idで指定される列の値)
            このリストの順番で描画される
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
    box_kwargs["hue_order"] = hue_order
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
        order=sample_filter,
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


def gen_line_mean_sd_graph(
    ax, data, sample_filter=[], order=None, sample_row_id=0, group_row_id=2
):
    """
    Args:
        ax: matplotlib.axes.Axes
            lineplotを描画するAxes
        data: pd.DataFrame
            描画するデータ
            schemeta_splitterで定義される転地形式にのみ対応
        sample_filter:
            描画するデータのサンプル名のリスト
            空の場合は全データを使用
        sample_row_id:
            dataのsample行のインデックス (schemeta_splitterで定義される転地形式のmain_idに対応: 0)
        group_row_id:
            dataのgroup行のインデックス (schemeta_splitterで定義される転地形式のgroupに対応: 2)
        order: List[str]
            描画するデータの順序
            group行のユニークな値のリスト

    Returns:
        ax: matplotlib.axes.Axes
            lineplotが描画されたAxes
    """
    line_kwargs = LINE_PLOT_SETTINGS.copy()

    long_data = convert_data_to_lineplot(
        data, sample_row_id, group_row_id, sample_filter
    )

    line_trp = trp.TrendPlots(ax)
    line_trp.add_line_mean_sd_plot(data=long_data, order=order, **line_kwargs)

    return line_trp.ax


def gen_individual_line_graph(
    ax, data, sample_filter=[], order=None, sample_row_id=0, group_row_id=2
):
    """
    Args:
        ax: matplotlib.axes.Axes
            lineplotを描画するAxes
        data: pd.DataFrame
            描画するデータ
            schemeta_splitterで定義される転地形式にのみ対応
        sample_filter:
            描画するデータのサンプル名のリスト
            空の場合は全データを使用
        sample_row_id:
            dataのsample行のインデックス (schemeta_splitterで定義される転地形式のmain_idに対応: 0)
        group_row_id:
            dataのgroup行のインデックス (schemeta_splitterで定義される転地形式のgroupに対応: 2)
        order: List[str]
            描画するデータの順序
            group行のユニークな値のリスト

    Returns:
        ax: matplotlib.axes.Axes
            lineplotが描画されたAxes
    """
    line_kwargs = LINE_PLOT_SETTINGS.copy()

    long_data = convert_data_to_lineplot(
        data, sample_row_id, group_row_id, sample_filter
    )

    line_trp = trp.TrendPlots(ax)
    line_trp.add_line_group_coloring_plot(data=long_data, order=order, **line_kwargs)

    return line_trp.ax
