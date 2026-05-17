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

    def solve_and_display(self, delay: float = 0.05) -> None:
        if not self.grid:
            raise RuntimeError("Call generate() before solve_and_display().")
        if self.solver is None:
            raise RuntimeError("No solver configured.")

        for start in self.entrances:
            for goal in self.exits:
                path, visited = self.solver.solve(self.grid, start, goal)
                label = f"Entrance {start} -> Exit {goal}"
                self._animate(visited, path, start, goal, label, delay)
                if path:
                    self._render(
                        set(visited), set(path), start, goal, label, current=None
                    )
                    print(
                        f"\nSolved in {len(path) - 1} steps  ({len(visited)} cells explored)"
                    )
                else:
                    print("\nNo path found.")
                time.sleep(1.0)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _animate(
        self,
        visited: list[tuple[int, int]],
        path: list[tuple[int, int]] | None,
        start: tuple[int, int],
        goal: tuple[int, int],
        label: str,
        delay: float,
    ) -> None:
        visited_set: set[tuple[int, int]] = set()
        path_set = set(path) if path else set()

        for i, cell in enumerate(visited):
            visited_set.add(cell)
            is_last = i == len(visited) - 1
            self._render(
                visited_set,
                path_set if is_last else set(),
                start,
                goal,
                label,
                current=None if is_last else cell,
            )
            time.sleep(delay)

    def _render(
        self,
        visited: set[tuple[int, int]],
        path: set[tuple[int, int]],
        start: tuple[int, int],
        goal: tuple[int, int],
        label: str,
        current: tuple[int, int] | None,
    ) -> None:
        os.system("clear")
        print("\033[H\033[J", end="", flush=True)
        print(label)
        print()

        grid = self.grid
        rows, cols = self.rows, self.cols

        for r in range(rows):
            # Horizontal wall line
            wall_line = ""
            for c in range(cols):
                wall_line += "+"
                wall_line += "  " if not grid[r][c].walls[NORTH] else "--"
            wall_line += "+"
            print(wall_line)

            # Cell content line
            cell_line = ""
            for c in range(cols):
                cell_line += " " if not grid[r][c].walls[WEST] else "|"
                pos = (r, c)
                if pos == start:
                    cell_line += "S "
                elif pos == goal:
                    cell_line += "E "
                elif pos == current:
                    cell_line += "@ "
                elif pos in path:
                    cell_line += "* "
                elif pos in visited:
                    cell_line += ". "
                else:
                    cell_line += "  "
            cell_line += " " if not grid[r][cols - 1].walls[EAST] else "|"
            print(cell_line)

        # Bottom wall line
        bottom = ""
        for c in range(cols):
            bottom += "+"
            bottom += "  " if not grid[rows - 1][c].walls[SOUTH] else "--"
        bottom += "+"
        print(bottom)

        print()
        print("S=start  E=exit  @=exploring  .=visited  *=solution path")
