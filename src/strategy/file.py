from pathlib import Path
from typing import TextIO

from src.strategy.base import OutputStrategy


class FileOutputStrategy(OutputStrategy):
    def __init__(self, output_path: Path, mode: str = "w", encoding: str = "utf-8") -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self._file: TextIO = output_path.open(mode, encoding=encoding)

    def write(self, record: str) -> None:
        self._file.write(f"{record}\n")

    def close(self) -> None:
        self._file.close()
