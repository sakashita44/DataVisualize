import pandas as pd
import yaml
import csv
import re
from typing import List
import schemeta_splitter.io as ss

from graphconfig import GraphConfig
from graphinstruction import BoxGraphInstruction, LineGraphInstruction


def read_config(config_path: str) -> GraphConfig:
    with open(config_path, encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    return GraphConfig(**config_data)


def read_box_instructions(instruction_path: str) -> List[BoxGraphInstruction]:
    instructions = []
    with open(instruction_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instruction = BoxGraphInstruction(
                output_name=row["output_name"],
                filename=row["filename"],
                dtype=row["dtype"],
                sample_filter=process_sample_filter(row["sample_filter"]),
                ylim_min=float(row["ylim_min"].strip())
                if row["ylim_min"].strip()
                else None,
                ylim_max=float(row["ylim_max"].strip())
                if row["ylim_max"].strip()
                else None,
                xlabel=row["xlabel"],
                ylabel=row["ylabel"],
                legends=process_legend(row["legends"]),
                brackets=process_brackets(row["brackets"]),
                bracket_base_y=float(row["bracket_base_y"])
                if row["bracket_base_y"]
                else None,
            )
            instructions.append(instruction)
    return instructions


def read_line_instructions(instruction_path: str) -> List[LineGraphInstruction]:
    instructions = []
    with open(instruction_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instruction = LineGraphInstruction(
                output_name=row["output_name"],
                filename=row["filename"],
                dtype=row["dtype"],
                sample_filter=process_sample_filter(row["sample_filter"]),
                xlim_min=float(row["xlim_min"].strip())
                if row["xlim_min"].strip()
                else None,
                xlim_max=float(row["xlim_max"].strip())
                if row["xlim_max"].strip()
                else None,
                ylim_min=float(row["ylim_min"].strip())
                if row["ylim_min"].strip()
                else None,
                ylim_max=float(row["ylim_max"].strip())
                if row["ylim_max"].strip()
                else None,
                xlabel=row["xlabel"],
                ylabel=row["ylabel"],
                legends=process_legend(row["legends"]),
            )
            instructions.append(instruction)
    return instructions


def process_sample_filter(sample_filter: str) -> List[str]:
    sample_filter = sample_filter.strip()
    if sample_filter == "":
        return []
    # sample_filterの形式が"(a)(b)(c)"の場合, ["a", "b", "c"]に変換
    # まず)をすべて削除
    sample_filter = re.sub(r"\)", "", sample_filter)
    # 先頭の(を削除
    sample_filter = sample_filter[1:]
    # (で分割
    sample_filter_list = sample_filter.split("(")
    # すべての要素をstrip
    sample_filter_list = [item.strip() for item in sample_filter_list]
    return sample_filter_list


def process_legend(legend: str) -> dict:
    legend = legend.strip()
    if legend == "":
        return {}
    # legendの形式が"(a:1)(b:2)"の場合, {"a": "1", "b": "2"}に変換
    # legendの形式が"(a:1)(:2)"の場合, {"a": "1", "": "2"}に変換
    # まず)をすべて削除
    legend = re.sub(r"\)", "", legend)
    # 先頭の(を削除
    legend = legend[1:]
    # (で分割
    legend_tmp = legend.split("(")
    # この時点でlegendは["a:1", "b:2"]のようなリストになっている
    legend_dict = {}
    for item in legend_tmp:
        # :で分割
        key, value = item.split(":")
        legend_dict[str(key.strip())] = str(value.strip())
    return legend_dict


def process_brackets(brackets: str) -> List[List]:
    brackets = brackets.strip()
    if brackets == "":
        return []
    # bracketsの形式が"([a:b][c:d]*)([w:x][y:z]+)"の場合, [[['a', 'b'], ['c', 'd'], '*'], [['w', 'x'], ['y', 'z'], '+']]に変換
    # まず)をすべて削除
    brackets = re.sub(r"\)", "", brackets)
    # 先頭の(を削除
    brackets = brackets[1:]
    # (で分割
    brackets_tmp = brackets.split("(")
    # この時点でbracketsは["[a:b][c:d]*", "[w:x][y:z]+"]のようなリストになっている
    brackets_list = []
    for item in brackets_tmp:
        # [を削除
        item = re.sub(r"\[", "", item)
        # ]で分割
        item = item.split("]")
        # この時点でitemは["a:b", "c:d", "*"]のようなリストになっている
        item_list = []
        for i in item:
            # :で分割
            i = i.split(":")
            # iのすべての要素をstrip
            i = [j.strip() for j in i]
            # iのすべての要素をstrに変換
            i = [str(j) for j in i]
            item_list.append(i)
            # item_listは[['a', 'b'], ['c', 'd'], ['*']]のようなリストになっている
        item_list[2] = item_list[2][0]
        # item_listを全体をlistからtupleに変換
        item_list = tuple(item_list)
        brackets_list.append(item_list)
    return brackets_list


def convert_data_to_lineplot(data, sample_row_id, group_row_id, sample_filter=[]):
    # sample_filterで指定されたサンプルのデータのみを抽出
    if len(sample_filter) > 0:
        # dataのsample_row_id行目の値がsample_filterに含まれない列を削除
        data = data.loc[:, data.iloc[sample_row_id, :].isin(sample_filter)]

    else:
        # sample_filterが空の場合はデータをそのまま使用
        pass

    # dataのgroup_row_id行の値を取得しlistに変換
    groups = data.iloc[group_row_id, :].tolist()

    # dataの上から3行を削除
    data = data.iloc[3:, :]

    # dataの列名をgroupsに変更
    data.columns = groups

    # dataのindexをfloatに変換
    data.index = data.index.astype(float)

    return data


def read_schemeta_data(path: str, dtype: str, graph_type: str) -> pd.DataFrame:
    if dtype == "tp":
        is_wide = False
    elif dtype == "wide":
        is_wide = True
    else:
        raise ValueError(f"dtype {dtype} is not supported")

    meta_df, data_df = ss.read_file(file_path=path, is_wide_format=is_wide)

    if graph_type == "box":
        get_wide_format = True
    elif graph_type == "line":
        get_wide_format = False
    else:
        raise ValueError(f"graph_type {graph_type} is not supported")

    concat_df = ss.concatenate_dataframes(
        meta_df=meta_df, data_df=data_df, get_wide_format=get_wide_format
    )

    return concat_df


def get_order(legends):
    # legendの指定がある場合はorderを指定
    if legends != {}:
        order = list(legends.keys())
    else:
        order = None

    return order
