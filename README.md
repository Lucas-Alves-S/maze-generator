# Maze Generator

A terminal-based maze generator and solver written in Python. Mazes are generated procedurally and solved with an animated step-by-step visualization rendered directly in the terminal.

## How it works

### Generation — Randomized Kruskal's algorithm

The maze is built on a grid of cells, each starting with all four walls intact. Kruskal's algorithm treats every cell as its own set and iterates over a shuffled list of internal walls. When a wall separates two cells that belong to different sets, the wall is removed and the sets are merged (union-find). The result is a **perfect maze**: every cell is reachable and there is exactly one path between any two cells.

### Solving — Greedy best-first search

Once the maze is generated, a configurable number of entrances and exits are punched through the border at random. The solver runs **greedy best-first search** from each entrance to each exit, using Manhattan distance as the heuristic. It returns both the final path and the order in which cells were explored, which drives the animation.

### Terminal animation

`solve_and_display` animates each entrance-exit pair one at a time:

- `S` — start (entrance)
- `E` — exit
- `@` — cell currently being explored
- `.` — visited cell
- `*` — solution path

After all pairs are animated, a combined view shows every solved path at once.

## Requirements

- Python 3.13+
- [`uv`](https://github.com/astral-sh/uv) (recommended) **or** a plain Python virtual environment

No third-party packages are required — the project uses only the standard library.

## Setup and running

### With uv (recommended)

```bash
git clone https://github.com/Lucas-Alves-S/maze-generator.git
cd maze-generator
uv run main.py
```

`uv` creates and manages the virtual environment automatically.

### Without uv

```bash
git clone https://github.com/Lucas-Alves-S/maze-generator.git
cd maze-generator
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python main.py
```

## Configuration

Edit the `main()` function in `main.py` to change maze parameters:

| Parameter | Default | Description |
|---|---|---|
| `rows` | `15` | Number of rows |
| `cols` | `30` | Number of columns |
| `num_entrances` | `4` | Entrances punched through the border |
| `num_exits` | `1` | Exits punched through the border |
| `delay` | `0.1` | Seconds between animation frames |

## Project structure

```
maze-generator/
├── main.py                   # Entry point
└── src/
    ├── cell.py               # Cell dataclass and direction constants
    ├── maze.py               # Maze class — generation, solving, rendering
    ├── generators/
    │   ├── base.py           # BaseGenerator abstract class
    │   └── kruskal.py        # Randomized Kruskal's algorithm
    └── solvers/
        ├── base.py           # BaseSolver abstract class
        └── greedy.py         # Greedy best-first search solver
```

New generators or solvers can be added by subclassing `BaseGenerator` or `BaseSolver` and swapping them into `main.py`.
