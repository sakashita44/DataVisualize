import os
import matplotlib.pyplot as plt
from gen_graph import GenBoxGraph, GenLineGraph
from data_processing import (
    read_box_instructions,
    read_line_instructions,
    read_config,
    read_schemeta_data,
    get_order,
)

VIS_ROOT_DIR = os.path.join(os.path.dirname(__file__), "..\\")
CONFIG_YML = os.path.join(VIS_ROOT_DIR, "config.yml")


def test_path(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def gen_graph():
    # config.ymlの読み込み
    config = read_config(CONFIG_YML)

    # パスの設定
    box_instruction_path = os.path.join(VIS_ROOT_DIR, config.box_instruction_file)
    line_instruction_path = os.path.join(VIS_ROOT_DIR, config.line_instruction_file)

    input_dir = os.path.join(VIS_ROOT_DIR, config.input_dir)
    # output_dir = os.path.join(VIS_ROOT_DIR, config.output_dir)

    # instructionファイルの読み込み
    box_instructions = read_box_instructions(box_instruction_path)
    line_instructions = read_line_instructions(line_instruction_path)

    for box_instruction in box_instructions:
        # データの読み込み
        data_path = os.path.join(input_dir, box_instruction.filename)
        data = read_schemeta_data(data_path, box_instruction.dtype, "box")
        # ラベルになる列を文字列に変換
        data = data.astype({data.columns[0]: str})
        data = data.astype({data.columns[2]: str})

        # グラフの描画
        print(f"genaration box graph: {box_instruction.output_name}")
        fig, ax = plt.subplots()
        gen_box_graph = GenBoxGraph(
            ax=ax,
            data=data,
            is_add_jitter=config.show_jitter,
            brackets=box_instruction.brackets,
            bracket_base_y=box_instruction.bracket_base_y,
            bracket_h_ratio=config.brackets_height_ratio,
            bracket_hspace_ratio=config.brackets_spacing_ratio,
            bracket_mark_fs=config.p_mark_font_size,
            sample_filter=box_instruction.sample_filter,
        )
        ax = gen_box_graph.get_box_graph()
        plt.show()

    for line_instruction in line_instructions:
        # データの読み込み
        data_path = os.path.join(input_dir, line_instruction.filename)
        data = read_schemeta_data(data_path, line_instruction.dtype, "line")
        order = get_order(line_instruction.legends)

        # グラフの描画
        print(f"genaration line graph: {line_instruction.output_name}")
        fig, ax = plt.subplots()
        gen_line_graph = GenLineGraph(
            ax=ax, data=data, sample_filter=line_instruction.sample_filter, order=order
        )
        ax = gen_line_graph.get_line_mean_sd_graph()
        plt.show()

    if config.save_individual:
        for line_instruction in line_instructions:
            # データの読み込み
            data_path = os.path.join(input_dir, line_instruction.filename)
            data = read_schemeta_data(data_path, line_instruction.dtype, "line")
            order = get_order(line_instruction.legends)

            # グラフの描画
            print(f"genaration individual line graph: {line_instruction.output_name}")
            fig, ax = plt.subplots()
            gen_line_graph = GenLineGraph(
                ax=ax,
                data=data,
                sample_filter=line_instruction.sample_filter,
                order=order,
            )
            ax = gen_line_graph.gen_individual_line_graph()
            plt.show()


if __name__ == "__main__":
    gen_graph()
