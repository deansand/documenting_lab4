import csv
import json
from pathlib import Path
from typing import Iterator


class LineDatasetReader:
    """Reads text dataset as non-empty, trimmed lines."""

    def __init__(self, input_path: Path, encoding: str = "utf-8") -> None:
        self._input_path = input_path
        self._encoding = encoding

    def read(self) -> Iterator[str]:
        with self._input_path.open("r", encoding=self._encoding) as file:
            for line in file:
                value = line.strip()
                if value:
                    yield value


class CsvDatasetReader:
    """Reads CSV dataset and yields each row as compact JSON string."""

    def __init__(self, input_path: Path, encoding: str = "utf-8", delimiter: str = ",") -> None:
        self._input_path = input_path
        self._encoding = encoding
        self._delimiter = delimiter

    def read(self) -> Iterator[str]:
        with self._input_path.open("r", encoding=self._encoding, newline="") as file:
            csv_reader = csv.DictReader(file, delimiter=self._delimiter)
            for row in csv_reader:
                yield json.dumps(row, ensure_ascii=False, separators=(",", ":"))
