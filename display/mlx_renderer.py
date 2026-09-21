from __future__ import annotations

import os

from mazegen.generator import Cell

from mlx_bindings import MLX

CELL_SIZE = 24
WALL_COLOR = 0xFFFFFF
ESC_KEYCODE = 65307


class MLXRenderer:

    def __init__(self, grid: list[list[Cell]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0
        self.mlx = MLX()

        self.window = self.mlx.new_window(
            max(self.width * CELL_SIZE + 1, 1),
            max(self.height * CELL_SIZE + 1, 1),
            "A-Maze-ing",
        )

    def draw_maze(self) -> None:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                self._draw_cell_walls(x, y, cell)

    def _draw_cell_walls(self, x: int, y: int, cell: Cell) -> None:
        left, top = x * CELL_SIZE, y * CELL_SIZE
        right, bottom = left + CELL_SIZE, top + CELL_SIZE
        if not cell.is_open("N"):
            self._draw_line(left, top, right, top)
        if not cell.is_open("W"):
            self._draw_line(left, top, left, bottom)
        if y == self.height - 1 and not cell.is_open("S"):
            self._draw_line(left, bottom, right, bottom)
        if x == self.width - 1 and not cell.is_open("E"):
            self._draw_line(right, top, right, bottom)

    def _draw_line(self, x1: int, y1: int, x2: int, y2: int) -> None:

        if x1 == x2:
            for y in range(y1, y2 + 1):
                self.mlx.pixel_put(self.window, x1, y, WALL_COLOR)
        else:
            for x in range(x1, x2 + 1):
                self.mlx.pixel_put(self.window, x, y1, WALL_COLOR)

    def _on_key(self, keycode: int) -> int:
        if keycode == ESC_KEYCODE:
            self.mlx.destroy_window(self.window)

            os._exit(0)
        # falta mapear outras teclas para regenerar / mostrar caminho /
        # trocar cores, uma vez que a janela basica estiver funcionando.
        return 0

    def run(self) -> None:
        try:
            self.draw_maze()
            self.mlx.on_key(self.window, self._on_key)
            self.mlx.loop()
        finally:
            self.mlx.destroy_window(self.window)


if __name__ == "__main__":
    from mazegen.generator import MazeGenerator

    generator = MazeGenerator(
        width=20, height=15,
        entry=(0, 0), exit_coord=(19, 14),
        perfect=False, seed=42,
    )
    MLXRenderer(generator.generate()).run()