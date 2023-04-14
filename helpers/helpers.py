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
