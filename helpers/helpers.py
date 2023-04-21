import re
import os
import yt_dlp

from PyQt5.QtWidgets import QMessageBox


def validate_float_input(ipt: str, inputname: str) -> bool:
    if not ipt:
        return True
    try:
        float(ipt)
        return True
    except ValueError:
        QMessageBox.critical(None, "Error", f"{inputname} needs to be a (decimal) number.")
        return False


def validate_start_end_time(start_time, end_time):
    if start_time is not None and end_time is not None:
        if start_time < end_time:
            return False
    return True


def strip_empty_to_none(ipt: str) -> None | str:
    if ipt.strip() == "":
        return None
    return ipt.strip()


def ytdl_download_soundtrack(url: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "./_temp/%(title)s.%(ext)s",
        "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_pattern = ydl.prepare_filename(info_dict)
        des = os.path.join(os.getcwd(), file_pattern)
        if not des.endswith(".wav"):
            des = os.path.splitext(des)[0] + ".wav"
    return des
