import unittest
from mazegen.encoder import (
    encode_maze,
    encode_grid,
    encode_cell,
    write_file
)
from mazegen.generator import Cell
import tempfile


class TestEncoder(unittest.TestCase):
    def test_encode_cell(self) -> None:
        cell = Cell(x=0, y=0, walls=15)
        result = encode_cell(cell)
        self.assertEqual(result, "F")
        
    def test_encode_grid(self) -> None:
        grid = [
            [
                Cell(x=0, y=0, walls=15),
                Cell(x=1, y=0, walls=10),
            ],
            [
                Cell(x=0, y=1, walls=0),
                Cell(x=1, y=1, walls=5),
            ],
        ]
        result = encode_grid(grid)
        self.assertEqual(result, ["FA", "05"])
    
    def test_encode_maze(self) -> None:
        grid = [
            [
                Cell(x=0, y=0, walls=15),
                Cell(x=1, y=0, walls=10),
            ],
            [
                Cell(x=0, y=1, walls=0),
                Cell(x=1, y=1, walls=5),
            ],
        ]
        result = encode_maze(
            grid=grid,
            entry=(0, 0),
            exit_coord=(1, 1),
            path=["E", "S"],
        )
        expected = "FA\n05\n\n0,0\n1,1\nES\n"
        self.assertEqual(result, expected)

    def test_write_file(self) -> None:
        cotent = "FA\n05\n\n0,0\n1,1\nES\n"
        with tempfile.TemporaryDirectory() as directory:
            out_path = f"{directory}/maze.txt"
            write_file(out_path, cotent)
            with open(out_path, "r", encoding="utf-8") as file:
                result = file.read()
        self.assertEqual(result, cotent)
