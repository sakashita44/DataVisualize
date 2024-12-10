from logging import config
import yaml
import csv
from typing import List

from graphconfig import GraphConfig
from graphinstruction import GraphInstruction


def read_config(config_path: str) -> GraphConfig:
    with open(config_path, encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    return GraphConfig(**config_data)


def read_instructions(instruction_path: str) -> List[GraphInstruction]:
    instructions = []
    with open(instruction_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["xlim_min"] = float(row["xlim_min"]) if row["xlim_min"] else None
            row["xlim_max"] = float(row["xlim_max"]) if row["xlim_max"] else None
            row["ylim_min"] = float(row["ylim_min"]) if row["ylim_min"] else None
            row["ylim_max"] = float(row["ylim_max"]) if row["ylim_max"] else None
            row["bracket_base_y"] = (
                float(row["bracket_base_y"]) if row["bracket_base_y"] else None
            )
            row["legend"] = (
                {
                    k: v
                    for k, v in (item.split(":") for item in row["legend"].split("."))
                }
                if row["legend"]
                else {}
            )
            row["brackets"] = (
                [
                    [list(map(int, b.split(":"))) for b in item.split("]") if b]
                    for item in row["brackets"].split(".")
                ]
                if row["brackets"]
                else []
            )
            instructions.append(GraphInstruction(**row))
    return instructions


if __name__ == "__main__":
    import os

    root = os.path.dirname(os.path.dirname(__file__))
    print(root)

    config_path = os.path.join(root, "config.yml")
    instruction_path = os.path.join(root, "Inputs/instructions.csv")

    print(read_config(config_path))
    # print(read_instructions(instruction_path))
