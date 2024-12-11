import os
import matplotlib.pyplot as plt
import pandas as pd
from gen_graph import GenBoxGraph, GenLineGraph
from data_processing import read_box_instructions, read_line_instructions, read_config

VIS_ROOT_DIR = os.path.join(os.path.dirname(__file__), "..\\")
CONFIG_YML = os.path.join(VIS_ROOT_DIR, "config.yml")


def test_path(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def gen_graph():
    config = read_config(CONFIG_YML)

    box_instruction_path = os.path.join(VIS_ROOT_DIR, config.box_instruction_file)
    line_instruction_path = os.path.join(VIS_ROOT_DIR, config.line_instruction_file)

    box_instructions = read_box_instructions(box_instruction_path)
    line_instructions = read_line_instructions(line_instruction_path)

    input_dir = os.path.join(VIS_ROOT_DIR, config.input_dir)
    output_dir = os.path.join(VIS_ROOT_DIR, config.output_dir)

    for box_instruction in box_instructions:
        data_path = os.path.join(input_dir, box_instruction.filename)
        data = pd.read_csv(data_path, index_col=0)
        fig, ax = plt.subplots()
        print(f"genaration box graph: {box_instruction.output_name}")
        data = data.astype({data.columns[0]: str})
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
        pass


if __name__ == "__main__":
    gen_graph()
