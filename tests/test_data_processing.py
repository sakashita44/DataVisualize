import unittest
import os
import sys
import pandas as pd
from unittest.mock import patch, mock_open

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from scripts.data_processing import (
    read_config,
    read_box_instructions,
    read_line_instructions,
    process_sample_filter,
    process_legend,
    process_brackets,
    convert_data_to_lineplot,
)

from scripts.graphinstruction import BoxGraphInstruction, LineGraphInstruction


class TestDataProcessing(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""
input_dir: 'Inputs'
output_dir: 'Outputs'
box_instruction_file: 'Inputs/box_instructions.csv'
line_instruction_file: 'Inputs/line_instructions.csv'
label_font_size: 20
tick_font_size: 15
legend_font_size: 15
xlabel_loc_x: 0.5
xlabel_loc_y: -0.1
ylabel_loc_x: -0.15
ylabel_loc_y: 0.5
graph_limit_left: 0.2
graph_limit_right: 0.9
graph_limit_bottom: 0.15
graph_limit_top: 0.9
figure_dpi: 100
figure_width: 8
figure_height: 6
mean_marker_type: '+'
mean_marker_size: 10
outlier_marker_type: 'x'
outlier_marker_size: 10
show_individual: True
jitter_marker_type: 'o'
jitter_marker_alpha: 0.7
jitter_marker_size: 5
show_significance_brackets: True
brackets_height_ratio: 0.02
brackets_spacing_ratio: 0.1
p_mark_font_size: 10
show_graph: True
save_describe: True
save_individual: True
""",
    )
    def test_read_config(self, mock_file):
        config = read_config("dummy_path")
        self.assertEqual(config.input_dir, "Inputs")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="output_name,filename,dtype,sample_filter,ylim_min,ylim_max,xlabel,ylabel,legends,brackets,bracket_base_y\n",
    )
    def test_read_box_instructions(self, mock_file):
        instructions = read_box_instructions("dummy_path")
        self.assertIsInstance(instructions, list)
        self.assertTrue(all(isinstance(i, BoxGraphInstruction) for i in instructions))

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="output_name,filename,dtype,sample_filter,xlim_min,xlim_max,ylim_min,ylim_max,xlabel,ylabel,legends\n",
    )
    def test_read_line_instructions(self, mock_file):
        instructions = read_line_instructions("dummy_path")
        self.assertIsInstance(instructions, list)
        self.assertTrue(all(isinstance(i, LineGraphInstruction) for i in instructions))

    def test_process_sample_filter(self):
        result = process_sample_filter("(a)(b)(c)")
        self.assertEqual(result, ["a", "b", "c"])

    def test_process_legend(self):
        result = process_legend("(a:1)(b:2)")
        self.assertEqual(result, {"a": "1", "b": "2"})

    def test_process_brackets(self):
        result = process_brackets("([a:b][c:d]*)([w:x][y:z]+)")
        self.assertEqual(
            result, [[["a", "b"], ["c", "d"], ["*"]], [["w", "x"], ["y", "z"], ["+"]]]
        )

    def test_convert_data_to_lineplot(self):
        data = pd.DataFrame(
            {
                "sample": ["a", "b", "c", "d"],
                "dummy": ["x", "y", "x", "y"],
                "group": ["x", "y", "x", "y"],
                0: [1, 2, 3, 4],
                1: [5, 6, 7, 8],
                2: [9, 10, 11, 12],
            }
        )
        data = data.T
        result = convert_data_to_lineplot(data, 0, 2, sample_filter=["a", "c"])
        self.assertEqual(result.columns.tolist(), ["x", "x"])
        self.assertEqual(result.index.tolist(), [0, 1, 2])

    def test_convert_data_to_lineplot_no_filter(self):
        data = pd.DataFrame(
            {
                "sample": ["a", "b", "c", "d"],
                "dummy": ["x", "y", "x", "y"],
                "group": ["x", "y", "x", "y"],
                0: [1, 2, 3, 4],
                1: [5, 6, 7, 8],
                2: [9, 10, 11, 12],
            }
        )
        data = data.T
        result = convert_data_to_lineplot(data, 0, 2)
        self.assertEqual(result.columns.tolist(), ["x", "y", "x", "y"])
        self.assertEqual(result.index.tolist(), [0, 1, 2])


if __name__ == "__main__":
    unittest.main()

    def test_read_box_instructions(self, mock_file):
        instructions = read_box_instructions("dummy_path")
        self.assertIsInstance(instructions, list)
        self.assertTrue(all(isinstance(i, BoxGraphInstruction) for i in instructions))

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="output_name,filename,dtype,sample_filter,xlim_min,xlim_max,ylim_min,ylim_max,xlabel,ylabel,legends\n",
    )
    def test_read_line_instructions(self, mock_file):
        instructions = read_line_instructions("dummy_path")
        self.assertIsInstance(instructions, list)
        self.assertTrue(all(isinstance(i, LineGraphInstruction) for i in instructions))

    def test_process_sample_filter(self):
        result = process_sample_filter("(a)(b)(c)")
        self.assertEqual(result, ["a", "b", "c"])

    def test_process_legend(self):
        result = process_legend("(a:1)(b:2)")
        self.assertEqual(result, {"a": "1", "b": "2"})

    def test_process_brackets(self):
        result = process_brackets("([a:b][c:d]*)([w:x][y:z]+)")
        self.assertEqual(
            result, [[["a", "b"], ["c", "d"], "*"], [["w", "x"], ["y", "z"], "+"]]
        )

    def test_convert_data_to_lineplot(self):
        data = pd.DataFrame(
            {
                "sample": ["a", "b", "c", "d"],
                "group": ["x", "y", "x", "y"],
                0: [1, 2, 3, 4],
                1: [5, 6, 7, 8],
                2: [9, 10, 11, 12],
            }
        )
        result = convert_data_to_lineplot(data, 0, 1, sample_filter=["a", "c"])
        self.assertEqual(result.columns.tolist(), ["x", "y"])
        self.assertEqual(result.index.tolist(), [3.0, 4.0])


if __name__ == "__main__":
    unittest.main()
