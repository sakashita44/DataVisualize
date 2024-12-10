from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class GraphInstruction:
    output_name: str
    filename: str
    dtype: str
    graph_type: str
    xlim_min: Optional[float]
    xlim_max: Optional[float]
    ylim_min: Optional[float]
    ylim_max: Optional[float]
    xlabel: str
    ylabel: str
    legend: Dict[str, str]
    brackets: List[List]
    bracket_base_y: Optional[float]
