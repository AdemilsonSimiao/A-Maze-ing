from dataclasses import dataclass
import random
from .algorithms import algorithm_names, generate_edges
from .pattern import plan_pattern


@dataclass
class Cell:
    x: int
    y: int
    walls: int = 15

    def is_open(self, direction: str) -> bool:
        bit = self._direction_bit(direction)
        return (self.walls & bit) == 0

    @staticmethod
    def _direction_bit(direction: str) -> int:
        bits = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8,
        }
        return bits[direction]


class MazeGenerator:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL_WALLS = NORTH | EAST | SOUTH | WEST
    ALGORITHMS = algorithm_names()
    DIRECTION_BITS = {
        "N": NORTH,
        "E": EAST,
        "S": SOUTH,
        "W": WEST,
    }
    DIRECTION_DELTAS = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }
    OPPOSITES = {
        "N": "S",
        "E": "W",
        "S": "N",
        "W": "E",
    }

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit_coord: tuple[int, int],
            perfect: bool = True,
            seed: int | None = None,
            algorithm: str = "dfs"
    ) -> None:
        if width < 1 or height < 1:
            raise ValueError("Maze width and height must be at least 1.")
        for name, (x, y) in (("Entry", entry), ("Exit", exit_coord)):
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"{name} is outside the maze bounds.")
        if entry == exit_coord:
            raise ValueError("Entry and exit must be different.")
        if algorithm not in self.ALGORITHMS:
            raise ValueError(
                f"Unknown algorithm '{algorithm}'. "
                f"Choose one of: {', '.join(self.ALGORITHMS)}."
            )
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_coord
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm
        self.random = random.Random(seed)
        self.grid: list[list[Cell]] = []
        self.pattern_cells: set[tuple[int, int]] = set()
        self.pattern_message = ""

    def _create_empty_grid(self) -> None:
        self.grid = [
            [
                Cell(x=x, y=y, walls=self.ALL_WALLS)
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def _open_passage(self, x1: int, y1: int, x2: int, y2: int) -> None:
        delta = (x2 - x1, y2 - y1)
        for direction, step in self.DIRECTION_DELTAS.items():
            if step == delta:
                opposite = self.OPPOSITES[direction]
                self.grid[y1][x1].walls &= ~self.DIRECTION_BITS[direction]
                self.grid[y2][x2].walls &= ~self.DIRECTION_BITS[opposite]
                return
        raise ValueError("Cells are not adjacent.")

    def _free_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[str, int, int]]:
        neighbors = []
        for direction, (dx, dy) in self.DIRECTION_DELTAS.items():
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue
            if (nx, ny) in self.pattern_cells:
                continue
            neighbors.append((direction, nx, ny))
        return neighbors

    def _free_positions(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for _, nx, ny in self._free_neighbors(x, y)]

    def _carve_tree(self) -> None:
        cells = [
            (cell.x, cell.y)
            for row in self.grid
            for cell in row
            if (cell.x, cell.y) not in self.pattern_cells
        ]
        passages = generate_edges(
            self.algorithm,
            cells,
            self.entry,
            lambda position: self._free_positions(*position),
            self.random,
        )
        for (x1, y1), (x2, y2) in passages:
            self._open_passage(x1, y1, x2, y2)

    def _block_is_open(self, left: int, top: int) -> bool:
        for row in range(3):
            for col in range(3):
                cell = self.grid[top + row][left + col]
                if col < 2 and not cell.is_open("E"):
                    return False
                if row < 2 and not cell.is_open("S"):
                    return False
        return True

    def _has_open_block_near(self, x: int, y: int) -> bool:
        for top in range(max(0, y - 2), min(y, self.height - 3) + 1):
            for left in range(max(0, x - 2), min(x, self.width - 3) + 1):
                if self._block_is_open(left, top):
                    return True
        return False

    def _try_open(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        first = self.grid[y1][x1]
        second = self.grid[y2][x2]
        saved = (first.walls, second.walls)
        self._open_passage(x1, y1, x2, y2)
        if self._has_open_block_near(x1, y1):
            first.walls, second.walls = saved
            return False
        return True

    def _is_dead_end(self, cell: Cell) -> bool:
        if (cell.x, cell.y) in self.pattern_cells:
            return False
        return bin(cell.walls).count("1") == 3

    def _is_not_dead_end_position(self, position: tuple[int, int]) -> bool:
        x, y = position
        return not self._is_dead_end(self.grid[y][x])

    def _closed_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (nx, ny)
            for direction, nx, ny in self._free_neighbors(x, y)
            if not self.grid[y][x].is_open(direction)
        ]

    def _remove_dead_ends(self) -> None:
        dead_ends = [
            cell
            for row in self.grid
            for cell in row
            if self._is_dead_end(cell)
        ]
        self.random.shuffle(dead_ends)
        for cell in dead_ends:
            if not self._is_dead_end(cell):
                continue
            options = self._closed_neighbors(cell.x, cell.y)
            self.random.shuffle(options)
            options.sort(key=self._is_not_dead_end_position)
            for nx, ny in options:
                if self._try_open(cell.x, cell.y, nx, ny):
                    break

    def _count_passages(self) -> int:
        return sum(
            cell.is_open("E") + cell.is_open("S")
            for row in self.grid
            for cell in row
        )

    def _add_extra_loops(self) -> None:
        free_cells = self.width * self.height - len(self.pattern_cells)
        target = max(2, free_cells // 10)
        extra = self._count_passages() - (free_cells - 1)
        closed_walls = []
        for row in self.grid:
            for cell in row:
                if (cell.x, cell.y) in self.pattern_cells:
                    continue
                for direction, nx, ny in self._free_neighbors(cell.x, cell.y):
                    if direction in ("E", "S") and not cell.is_open(direction):
                        closed_walls.append((cell.x, cell.y, nx, ny))
        self.random.shuffle(closed_walls)
        for x, y, nx, ny in closed_walls:
            if extra >= target:
                break
            if self._try_open(x, y, nx, ny):
                extra += 1

    def generate(self) -> list[list[Cell]]:
        self._create_empty_grid()
        self.pattern_cells, self.pattern_message = plan_pattern(
            self.width, self.height, self.entry, self.exit
        )
        if self.pattern_message:
            print(self.pattern_message)
        self._carve_tree()
        if not self.perfect:
            self._remove_dead_ends()
            self._add_extra_loops()
        return self.grid