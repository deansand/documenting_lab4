from src.config import OutputConfig
from src.strategy.base import OutputStrategy
from src.strategy.console import ConsoleOutputStrategy
from src.strategy.file import FileOutputStrategy
from src.strategy.kafka import KafkaOutputStrategy
from src.strategy.redis_store import RedisOutputStrategy


class UnsupportedOutputError(ValueError):
    pass


def create_output_strategy(output_cfg: OutputConfig) -> OutputStrategy:
    strategy_name = output_cfg.output_type

    if strategy_name == "console":
        return ConsoleOutputStrategy()

    if strategy_name == "file":
        return FileOutputStrategy(
            output_path=output_cfg.file.output_path,
            mode=output_cfg.file.mode,
            encoding=output_cfg.file.encoding,
        )

    if strategy_name == "kafka":
        return KafkaOutputStrategy(
            bootstrap_servers=output_cfg.kafka.bootstrap_servers,
            topic=output_cfg.kafka.topic,
        )

    if strategy_name == "redis":
        return RedisOutputStrategy(
            host=output_cfg.redis.host,
            port=output_cfg.redis.port,
            db=output_cfg.redis.db,
            list_key=output_cfg.redis.list_key,
        )

    raise UnsupportedOutputError(
        f"Unsupported output strategy: '{strategy_name}'. "
        "Allowed values: console, file, kafka, redis."
    )
