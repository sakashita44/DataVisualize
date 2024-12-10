from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class BoxGraphInstruction:
    output_name: str
    filename: str
    dtype: str
    sample_filter: List[str]
    ylim_min: Optional[float]
    ylim_max: Optional[float]
    xlabel: str
    ylabel: str
    legends: Dict[str, str]
    brackets: List[List]
    bracket_base_y: Optional[float]


@dataclass
class LineGraphInstruction:
    output_name: str
    filename: str
    dtype: str
    sample_filter: List[str]
    xlim_min: Optional[float]
    xlim_max: Optional[float]
    ylim_min: Optional[float]
    ylim_max: Optional[float]
    xlabel: str
    ylabel: str
    legends: Dict[str, str]
