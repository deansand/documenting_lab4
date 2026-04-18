import os
import sys
from pathlib import Path

from src.config import load_config
from src.dataset_fetcher import download_socrata_csv
from src.reader import CsvDatasetReader, LineDatasetReader
from src.strategy.factory import create_output_strategy


def _create_reader(config):
    if config.reader.reader_type == "line":
        return LineDatasetReader(
            input_path=config.reader.input_path,
            encoding=config.reader.encoding,
        )

    if config.reader.reader_type == "csv":
        return CsvDatasetReader(
            input_path=config.reader.input_path,
            encoding=config.reader.encoding,
            delimiter=config.reader.delimiter,
        )

    raise ValueError(
        f"Unsupported reader type: '{config.reader.reader_type}'. "
        "Allowed values: line, csv."
    )


def _prepare_dataset(config) -> None:
    if not config.dataset.enabled:
        return

    if config.dataset.reuse_existing and config.dataset.output_path.exists():
        return

    if config.dataset.source_type != "socrata_csv":
        raise ValueError(
            f"Unsupported dataset source type: '{config.dataset.source_type}'. "
            "Allowed values: socrata_csv."
        )

    if not config.dataset.url:
        raise ValueError("Dataset URL is required when dataset.enabled=true.")

    download_socrata_csv(
        url=config.dataset.url,
        output_path=config.dataset.output_path,
        page_size=config.dataset.page_size,
    )


def run(config_path: str | Path = "config.yaml") -> None:
    config = load_config(config_path)
    _prepare_dataset(config)

    reader = _create_reader(config)
    strategy = create_output_strategy(config.output)

    try:
        for record in reader.read():
            strategy.write(record)
    finally:
        strategy.close()


if __name__ == "__main__":
    cli_config_path = sys.argv[1] if len(sys.argv) > 1 else None
    env_config_path = os.getenv("APP_CONFIG")
    run(cli_config_path or env_config_path or "config.yaml")
