from abc import ABC, abstractmethod


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, record: str) -> None:
        raise NotImplementedError

    def close(self) -> None:
        """Optional resource cleanup hook for concrete strategies."""
        return
