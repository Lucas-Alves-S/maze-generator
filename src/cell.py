from dataclasses import dataclass, field

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
DIRECTIONS = {NORTH: (-1, 0), SOUTH: (1, 0), EAST: (0, 1), WEST: (0, -1)}


@dataclass
class Cell:
    row: int
    col: int
    walls: dict = field(
        default_factory=lambda: {NORTH: True, SOUTH: True, EAST: True, WEST: True}
    )
