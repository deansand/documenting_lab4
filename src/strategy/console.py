from src.strategy.base import OutputStrategy


class ConsoleOutputStrategy(OutputStrategy):
    def write(self, record: str) -> None:
        print(record)
