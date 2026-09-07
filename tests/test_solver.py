import unittest
from mazegen.generator import MazeGenerator, Cell
from mazegen.solver import MazeSolver

class TestMazeSolver(unittest.TestCase):
    def test_solver_finds_path(self) -> None:
        generator = MazeGenerator(
            width=3,
            height=3,
            entry=(0, 0),
            exit_coord=(2, 2),
            perfect=True,
            seed=42,
        )
        grid = generator.generate()
        solver = MazeSolver(
            grid=grid,
            entry=(0, 0),
            exit_coord=(2, 2),
        )
        path = solver.solve()
        self.assertTrue(path)
    
    def test_solution_reanches_exit(self) -> None:
        generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit_coord=(2, 2),
        perfect=True,
        seed=42,
        )
        grid = generator.generate()
        solver = MazeSolver(
            grid=grid,
            entry=(0, 0),
            exit_coord=(2, 2),
        )
        path = solver.solve()
        position = (0, 0)
        deltas = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        for direction in path:
            dx, dy = deltas[direction]
            position = (position[0] + dx, position[1] + dy)
        self.assertEqual(position, (2, 2))

    def test_no_path(self) -> None:
        grid = [
            [Cell(0, 0), Cell(1, 0)],
            [Cell(0, 1), Cell(1, 1)],
        ]
        solver = MazeSolver(
                grid=grid,
                entry=(0, 0),
                exit_coord=(1, 1),
            )
        self.assertEqual(solver.solve(), [])

if __name__ == "__main__":
    unittest.main()