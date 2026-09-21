import unittest
from display.ascii_renderer import render_maze, _build_path_positions
from mazegen.generator import Cell

class TestAsciiRenderer(unittest.TestCase):
    def test_single_cell(self) -> None:
        grid = [[Cell(0, 0)]]
        result = render_maze(
            grid=grid,
            entry=(0, 0),
            exit_coord=(0, 0),
            path=[],
        )
        expected = (
            "+---+\n"
            "| X |\n"
            "+---+\n"
        )
        self.assertEqual(result, expected)
    
    def test_connected_cells(self) -> None:
        grid = [[
            Cell(0, 0, walls=13),
            Cell(1, 0, walls=7),
        ]]
        result = render_maze(
            grid=grid,
            entry=(0, 0),
            exit_coord=(1, 0),
            path=["E"],
        )
        expected = (
            "+---+---+\n"
            "| E   X |\n"
            "+---+---+\n"
        )
        self.assertEqual(result, expected)
    
    def test_without_path(self) -> None:
        grid = [[
            Cell(0, 0, walls=13),
            Cell(1, 0, walls=5),
            Cell(2, 0, walls=7),
        ]]
        result = render_maze(
            grid=grid,
            entry=(0, 0),
            exit_coord=(2, 0),
            path=["E", "E"],
            show_path=False,
        )
        expected = (
            "+---+---+---+\n"
            "| E       X |\n"
            "+---+---+---+\n"
        )
        self.assertEqual(result, expected)
    
    def test_build_path_positions(self) -> None:
        result = _build_path_positions(
            entry=(1, 1),
            path=["E", "S", "W", "N"],
        )
        expected = {
            (1, 1),
            (2, 1),
            (2, 2),
            (1, 2),
        }
        self.assertEqual(result, expected)
