import re
import os
import subprocess

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


def strip_empty_to_none(ipt: str) -> None | str:
    if ipt.strip() == "":
        return None
    return ipt.strip()


def ytdl_download_soundtrack(url: str) -> str:
    dl = subprocess.run(["yt-dlp", "-o", "./_temp/%(title)s.%(ext)s", "-x", "--audio-format", "wav", url], capture_output=True, text=True)
    des = re.findall(r"\[ExtractAudio\] Destination: (.*?) \(pass -k to", str(dl))[0]
    if "\\nDeleting original" in des:
        des = des.split("\\nDeleting original")[0]
    return os.path.normpath(des.strip())