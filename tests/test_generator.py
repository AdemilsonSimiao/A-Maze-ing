import unittest
from mazegen.generator import MazeGenerator, Cell


class TestMazeGenerator(unittest.TestCase):
    def make_generator(self, perfect: bool) -> MazeGenerator:
        return MazeGenerator(
            width=5,
            height=3,
            entry=(0, 0),
            exit_coord=(4, 2),
            perfect=perfect,
            seed=42,
        )
    
    def setUp(self) -> None:
        self.generator = self.make_generator(perfect=True)
        self.grid = self.generator.generate()

    def test_grid_size(self) -> None:
        self.assertEqual(len(self.grid), 3)
        self.assertEqual(len(self.grid[0]), 5)

    def test_grid_contains_cells(self) -> None:
        self.assertIsInstance(self.grid[0][0], Cell)

    def test_same_seed_generators(self) -> None:
        first_generator = self.make_generator(perfect=True)
        second_generator = self.make_generator(perfect=True)
        first_grid = first_generator.generate()
        second_grid = second_generator.generate()
        first_walls = [
            [cell.walls for cell in row]
            for row in first_grid
        ]
        second_walls = [
            [cell.walls for cell in row]
            for row in second_grid
        ]
        self.assertEqual(first_walls, second_walls)

    def test_imperfect_maze(self) -> None:
        generator = self.make_generator(perfect=False)
        grid = generator.generate()
        self.assertEqual(len(grid), 3)
        self.assertEqual(len(grid[0]), 5)
    
    def test_walls_are_coherent(self) -> None:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if x + 1 < len(row):
                    east_cell = row[x + 1]
                    self.assertEqual(
                        cell.is_open("E"),
                        east_cell.is_open("W"),
                    )
                if y + 1 < len(self.grid):
                    south_cell = self.grid[y + 1][x]
                    self.assertEqual(
                        cell.is_open("S"),
                        south_cell.is_open("N"),
                    )
    
    def test_outer_borders_are_closed(self) -> None:
        for row in self.grid:
            self.assertFalse(row[0].is_open("W"))
            self.assertFalse(row[-1].is_open("E"))
        for cell in self.grid[0]:
            self.assertFalse(cell.is_open("N"))
        for cell in self.grid[-1]:
            self.assertFalse(cell.is_open("S"))
    
    
    
if __name__ == "__main__":
    unittest.main()
