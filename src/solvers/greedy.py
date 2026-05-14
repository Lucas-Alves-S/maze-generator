import heapq
from solvers.base import BaseSolver
from cell import DIRECTIONS


class GreedySolver(BaseSolver):
    """Greedy best-first search using Manhattan distance heuristic."""

    def solve(
        self,
        grid: list[list],
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> tuple[list[tuple[int, int]] | None, list[tuple[int, int]]]:
        rows, cols = len(grid), len(grid[0])

        def heuristic(pos: tuple[int, int]) -> int:
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

        counter = 0
        heap = [(heuristic(start), counter, start)]
        came_from: dict[tuple, tuple | None] = {start: None}
        visited_order: list[tuple[int, int]] = []

        while heap:
            _, _, current = heapq.heappop(heap)
            visited_order.append(current)

            if current == goal:
                path: list[tuple[int, int]] = []
                node: tuple[int, int] | None = current
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                return list(reversed(path)), visited_order

            r, c = current
            for direction, (dr, dc) in DIRECTIONS.items():
                if grid[r][c].walls[direction]:
                    continue
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                neighbor = (nr, nc)
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    counter += 1
                    heapq.heappush(heap, (heuristic(neighbor), counter, neighbor))

        return None, visited_order
