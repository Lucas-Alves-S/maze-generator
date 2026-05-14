import random
from generators.base import BaseGenerator
from cell import Cell, NORTH, SOUTH, EAST, WEST


class RandomizedKruskal(BaseGenerator):
    """Generates a perfect maze using randomized Kruskal's algorithm (union-find)."""

    def generate(self, rows: int, cols: int) -> list[list[Cell]]:
        grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

        parent = {(r, c): (r, c) for r in range(rows) for c in range(cols)}
        rank = {(r, c): 0 for r in range(rows) for c in range(cols)}

        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]

        def union(a, b) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        walls: list[tuple] = []
        for r in range(rows):
            for c in range(cols):
                if r + 1 < rows:
                    walls.append(((r, c), (r + 1, c), SOUTH, NORTH))
                if c + 1 < cols:
                    walls.append(((r, c), (r, c + 1), EAST, WEST))

        random.shuffle(walls)

        for (r1, c1), (r2, c2), d1, d2 in walls:
            if union((r1, c1), (r2, c2)):
                grid[r1][c1].walls[d1] = False
                grid[r2][c2].walls[d2] = False

        return grid
