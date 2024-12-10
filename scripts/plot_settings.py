import trplots as trp

## デフォルト設定

# 箱ひげ図作成時の設定 (sns.boxplotの引数`**kwargs`に渡す辞書)
BOX_PLOT_SETTINGS = {}

# (外れ値を除いた)平均値を示す点の設定 (matplotlib.plotの引数`**kwargs`に渡す辞書)
MEAN_PLOT_SETTINGS = trp.PLOT_DEFAULTS.copy()
# trp.PLOT_DEFAULTS = {
#     "color": "black",
#     "marker": "+",
#     "markersize": 10,
#     "markeredgewidth": 1,
# }

# 外れ値を示す点の設定 (sns.boxplotの引数`flierprops`に渡す辞書)
OUTLIER_PLOT_SETTINGS = trp.FLIERPROPS_DEFAULTS.copy()
# trp.FLIERPROPS_DEFAULTS = {"marker": "x", "markersize": 10}

# 箱ひげ図に追加するジッターの設定 (sns.swarmplotの引数`**kwargs`に渡す辞書)
SWARM_PLOT_SETTINGS = trp.SWARMPLOT_DEFAULTS.copy()
# trp.SWARMPLOT_DEFAULTS = {
#     "marker": "o",
#     "alpha": 0.7,
#     "linewidth": 1,
# }

# 線グラフの設定 (sns.lineplotの引数`**kwargs`に渡す辞書)
LINE_PLOT_SETTINGS = {}

## カスタマイズ設定

# example
# MEAN_PLOT_SETTINGS['color'] = 'black'
