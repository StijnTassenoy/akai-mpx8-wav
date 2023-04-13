# Python Imports #
import os
from dataclasses import dataclass


@dataclass
class SoundEffect:
    source_path: str
    output_path: str
    output_name: str
    start_time: int = None
    end_time: int = None

    def generate_output_path(self):
        if self.output_name:
            output_file_name = self.source_path.split(os.path.basename(self.source_path))[0]
            output_file_name += self.output_name
        else:
            output_file_name = self.source_path.rsplit(".")[0] + "_new"

        output_file_path = os.path.join(self.output_path, output_file_name)
        if not output_file_path.endswith(".wav"):
            output_file_path += ".wav"
        return output_file_path
