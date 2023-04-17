import subprocess

from helpers.helpers import ytdl_download_soundtrack


def edit_audio(start_time: float | None, end_time: float | None, input_file: str, output_file: str):
    # Use ffprobe to get the duration of the input file
    probe = subprocess.run(["ffprobe", "-show_format", "-i", input_file], capture_output=True, text=True)
    duration_str = next((s for s in probe.stdout.split() if "duration" in s), None)
    if duration_str is None:
        raise ValueError("Failed to get duration of input file.")
    duration = float(duration_str.split("=")[1])

    # Check if start_time and end_time are valid
    if start_time is not None and (float(start_time) < 0 or float(start_time) > duration):
        raise ValueError("Invalid start_time.")
    if end_time is not None and (float(end_time) < 0 or float(end_time) > duration):
        raise ValueError("Invalid end_time.")

    # Construct the ffmpeg command based on the input parameters
    cmd = ["ffmpeg", "-i", input_file]
    if start_time is not None:
        cmd += ["-ss", str(start_time)]
    if end_time is not None:
        cmd += ["-to", str(end_time)]
    cmd += ["-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2", output_file]

    # Run the ffmpeg command
    subprocess.run(cmd)
