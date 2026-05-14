from abc import ABC, abstractmethod
from cell import Cell


class BaseSolver(ABC):
    @abstractmethod
    def solve(
        self,
        grid: list[list[Cell]],
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> tuple[list[tuple[int, int]] | None, list[tuple[int, int]]]:
        """Return (path, visited_order). path is None if no solution exists."""
        ...
