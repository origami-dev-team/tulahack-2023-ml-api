from typing import Tuple

def parse_filename(filename: str) -> Tuple[str, str]:
    tokens = filename.split(".")
    ext = tokens[-1]
    name = tokens[:-1]
    return "".join(name), ext