from dataclasses import dataclass


@dataclass
class GraphConfig:
    input_dir: str
    output_dir: str
    box_instruction_file: str
    line_instruction_file: str
    label_font_size: int
    tick_font_size: int
    legend_font_size: int
    xlabel_loc_x: float
    xlabel_loc_y: float
    ylabel_loc_x: float
    ylabel_loc_y: float
    graph_limit_left: float
    graph_limit_right: float
    graph_limit_bottom: float
    graph_limit_top: float
    figure_dpi: int
    figure_width: float
    figure_height: float
    mean_marker_type: str
    mean_marker_size: int
    outlier_marker_type: str
    outlier_marker_size: int
    show_individual: bool
    jitter_marker_type: str
    jitter_marker_alpha: float
    jitter_marker_size: int
    show_significance_brackets: bool
    brackets_height_ratio: float
    brackets_spacing_ratio: float
    p_mark_font_size: int
    show_graph: bool
    save_describe: bool
    save_individual: bool
