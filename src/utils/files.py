from pathlib import Path


def get_files_by_extension(path: str, extension: str):
    return list(Path(path).rglob(f"*.{extension}"))
