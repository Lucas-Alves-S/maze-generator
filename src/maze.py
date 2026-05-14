import random
import time
import os
from cell import NORTH, SOUTH, EAST, WEST
from generators.base import BaseGenerator
from solvers.base import BaseSolver


class Maze:
    def __init__(
        self,
        rows: int,
        cols: int,
        num_entrances: int = 1,
        num_exits: int = 1,
        generator: BaseGenerator | None = None,
        solver: BaseSolver | None = None,
    ):
        self.rows = rows
        self.cols = cols
        self.num_entrances = num_entrances
        self.num_exits = num_exits
        self.generator = generator
        self.solver = solver
        self.grid: list[list] = []
        self.entrances: list[tuple[int, int]] = []
        self.exits: list[tuple[int, int]] = []

    def generate(self) -> None:
        if self.generator is None:
            raise RuntimeError("No generator configured.")
        self.grid = self.generator.generate(self.rows, self.cols)
        self._place_entrances_exits()

    def _place_entrances_exits(self) -> None:
        border: list[tuple[int, int, str]] = []
        for c in range(self.cols):
            border.append((0, c, NORTH))
            border.append((self.rows - 1, c, SOUTH))
        for r in range(self.rows):
            border.append((r, 0, WEST))
            border.append((r, self.cols - 1, EAST))

        total = self.num_entrances + self.num_exits
        chosen = random.sample(border, min(total, len(border)))

        for i, (r, c, side) in enumerate(chosen):
            self.grid[r][c].walls[side] = False
            if i < self.num_entrances:
                self.entrances.append((r, c))
            else:
                self.exits.append((r, c))


