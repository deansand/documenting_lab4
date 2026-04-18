from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ReaderConfig:
    reader_type: str
    input_path: Path
    encoding: str = "utf-8"
    delimiter: str = ","


@dataclass(frozen=True)
class DatasetConfig:
    enabled: bool
    source_type: str
    url: str
    output_path: Path
    page_size: int = 50000
    reuse_existing: bool = True


@dataclass(frozen=True)
class FileOutputConfig:
    output_path: Path
    mode: str = "w"
    encoding: str = "utf-8"


@dataclass(frozen=True)
class KafkaOutputConfig:
    bootstrap_servers: list[str]
    topic: str


@dataclass(frozen=True)
class RedisOutputConfig:
    host: str
    port: int
    db: int
    list_key: str


@dataclass(frozen=True)
class OutputConfig:
    output_type: str
    file: FileOutputConfig
    kafka: KafkaOutputConfig
    redis: RedisOutputConfig


@dataclass(frozen=True)
class AppConfig:
    dataset: DatasetConfig
    reader: ReaderConfig
    output: OutputConfig


def _resolve_path(raw_path: str, base_dir: Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def load_config(config_path: str | Path) -> AppConfig:
    cfg_path = Path(config_path).resolve()
    base_dir = cfg_path.parent

    with cfg_path.open("r", encoding="utf-8") as file:
        raw: dict[str, Any] = yaml.safe_load(file)

    reader_raw = raw["reader"]
    dataset_raw = raw.get("dataset", {})
    output_raw = raw["output"]

    dataset = DatasetConfig(
        enabled=bool(dataset_raw.get("enabled", False)),
        source_type=dataset_raw.get("type", "socrata_csv").strip().lower(),
        url=dataset_raw.get("url", ""),
        output_path=_resolve_path(dataset_raw.get("output_path", "./data/input.txt"), base_dir),
        page_size=int(dataset_raw.get("page_size", 50000)),
        reuse_existing=bool(dataset_raw.get("reuse_existing", True)),
    )

    reader = ReaderConfig(
        reader_type=reader_raw.get("type", "line").strip().lower(),
        input_path=_resolve_path(reader_raw["input_path"], base_dir),
        encoding=reader_raw.get("encoding", "utf-8"),
        delimiter=reader_raw.get("delimiter", ","),
    )

    file_raw = output_raw.get("file", {})
    file_cfg = FileOutputConfig(
        output_path=_resolve_path(file_raw.get("output_path", "./data/output.txt"), base_dir),
        mode=file_raw.get("mode", "w"),
        encoding=file_raw.get("encoding", "utf-8"),
    )

    kafka_raw = output_raw.get("kafka", {})
    kafka_cfg = KafkaOutputConfig(
        bootstrap_servers=kafka_raw.get("bootstrap_servers", ["localhost:9092"]),
        topic=kafka_raw.get("topic", "dataset-lines"),
    )

    redis_raw = output_raw.get("redis", {})
    redis_cfg = RedisOutputConfig(
        host=redis_raw.get("host", "localhost"),
        port=int(redis_raw.get("port", 6379)),
        db=int(redis_raw.get("db", 0)),
        list_key=redis_raw.get("list_key", "dataset:lines"),
    )

    output = OutputConfig(
        output_type=output_raw["type"].strip().lower(),
        file=file_cfg,
        kafka=kafka_cfg,
        redis=redis_cfg,
    )

    return AppConfig(dataset=dataset, reader=reader, output=output)
