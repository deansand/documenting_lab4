from kafka import KafkaProducer

from src.strategy.base import OutputStrategy


class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers: list[str], topic: str) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: value.encode("utf-8"),
        )
        self._topic = topic

    def write(self, record: str) -> None:
        self._producer.send(self._topic, record)

    def close(self) -> None:
        self._producer.flush()
        self._producer.close()
