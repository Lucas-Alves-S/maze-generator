from abc import ABC, abstractmethod
from cell import Cell


class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, rows: int, cols: int) -> list[list[Cell]]: ...
