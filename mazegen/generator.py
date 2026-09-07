from dataclasses import dataclass
import random


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

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit_coord: tuple[int, int],
            perfect: bool = True,
            seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_coord
        self.perfect = perfect
        self.seed = seed
        self.random = random.Random(seed)
        self.grid: list[list[Cell]] = []

    def _create_empty_grid(self) -> None:
        self.grid = [
            [
                Cell(x=x, y=y, walls=self.ALL_WALLS)
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def _open_passage(self, x1: int, y1: int, x2: int, y2: int) -> None:
        dx = x2 - x1
        dy = y2 - y1
        if dx == 1 and dy == 0:
            direct1 = "E"
            direct2 = "W"
        elif dx == -1 and dy == 0:
            direct1 = "W"
            direct2 = "E"
        elif dx == 0 and dy == 1:
            direct1 = "S"
            direct2 = "N"
        elif dx == 0 and dy == -1:
            direct1 = "N"
            direct2 = "S"
        else:
            raise ValueError("Cells are not adjacent.")
        self.grid[y1][x1].walls &= ~self.DIRECTION_BITS[direct1]
        self.grid[y2][x2].walls &= ~self.DIRECTION_BITS[direct2]

    def _generate_perfect_maze(self) -> None:
        self._create_empty_grid()
        visited = {self.entry}
        stack = [self.entry]

        while stack:
            x, y = stack[-1]
            neighbors = []
            for direction, (dx, dy) in self.DIRECTION_DELTAS.items():
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        neighbors.append((direction, nx, ny))
            if not neighbors:
                stack.pop()
                continue
            _, nx, ny = self.random.choice(neighbors)
            self._open_passage(x, y, nx, ny)
            visited.add((nx, ny))
            stack.append((nx, ny))

    def _add_loops(self) -> None:
        loop_budget = max(1, (self.width * self.height) // 12)
        for _ in range(loop_budget):
            x = self.random.randint(1, self.width - 2)
            y = self.random.randint(1, self.height - 2)
            options = []
            for direction, (dx, dy) in self.DIRECTION_DELTAS.items():
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    options.append((direction, nx, ny))
            if not options:
                continue
            direction, nx, ny = self.random.choice(options)
            if not self.grid[y][x].is_open(direction):
                self._open_passage(x, y, nx, ny)

    def generate(self) -> list[list[Cell]]:
        self._generate_perfect_maze()
        if not self.perfect:
            self._add_loops()
        return self.grid
