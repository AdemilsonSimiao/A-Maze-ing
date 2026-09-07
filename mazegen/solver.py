from collections import deque
from .generator import Cell


class MazeSolver:
    def __init__(
        self,
        grid: list[list[Cell]],
        entry: tuple[int, int],
        exit_coord: tuple[int, int],
    ) -> None:
        self.grid = grid
        self.entry = entry
        self.exit = exit_coord
    DIRECTION_DELTAS = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    def solve(self) -> list[str]:
        queue = deque([self.entry])
        visited = {self.entry}
        previous = {}
        while queue:
            current = queue.popleft()
            x, y = current
            if current == self.exit:
                break
            for direction, (dx, dy) in self.DIRECTION_DELTAS.items():
                nx = x + dx
                ny = y + dy
                if not (
                    0 <= nx < len(self.grid[0])
                    and 0 <= ny < len(self.grid)
                ):
                    continue
                neighbor = (nx, ny)
                if neighbor in visited:
                    continue
                if not self.grid[y][x].is_open(direction):
                    continue
                previous[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
        if self.exit not in previous:
            return []
        path = []
        current = self.exit
        while current != self.entry:
            previous_position = previous[current]
            px, py = previous_position
            dx = current[0] - px
            dy = current[1] - py
            if (dx, dy) == (0, -1):
                path.append("N")
            elif (dx, dy) == (1, 0):
                path.append("E")
            elif (dx, dy) == (0, 1):
                path.append("S")
            elif (dx, dy) == (-1, 0):
                path.append("W")
            current = previous_position
        path.reverse()
        return path
