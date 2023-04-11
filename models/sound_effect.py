# Python Imports #
from dataclasses import dataclass


@dataclass
class SoundEffect:
    source_path: str
    output_path: str
    output_name: str
    cut_from: int = None
    cut_to: int = None
