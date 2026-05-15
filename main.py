import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.maze import Maze
from src.generators.kruskal import RandomizedKruskal
from src.solvers.greedy import GreedySolver


def main():
    maze = Maze(
        rows=15,
        cols=30,
        num_entrances=4,
        num_exits=1,
        generator=RandomizedKruskal(),
        solver=GreedySolver(),
    )
    maze.generate()
    maze.solve_and_display(
        delay=0.1
    )  # TODO: function to call the solver and display the solution step by step


if __name__ == "__main__":
    main()
