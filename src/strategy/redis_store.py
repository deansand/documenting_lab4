import redis

from src.strategy.base import OutputStrategy


class RedisOutputStrategy(OutputStrategy):
    def __init__(self, host: str, port: int, db: int, list_key: str) -> None:
        self._client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self._list_key = list_key

    def write(self, record: str) -> None:
        self._client.rpush(self._list_key, record)
