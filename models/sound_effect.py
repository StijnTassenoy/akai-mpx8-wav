# Python Imports #
import json
from dataclasses import dataclass


@dataclass
class SoundEffect:
    source_path: str
    output_path: str
    output_name: str
    start_time: int = None
    end_time: int = None

