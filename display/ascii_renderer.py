from mazegen.generator import Cell


def _build_path_positions(
    entry: tuple[int, int],
    path: list[str],
) -> set[tuple[int, int]]:
    ...


def _horizon_line(row: list[Cell], direction: str) -> str:
    ...

def _middle_line(
    row: list[Cell],
    y: int,
    markers: dict[tuple[int, int], str],
) -> str:
    ...

def render_maze(
    grid: list[list[Cell]],
    entry: tuple[int, int],
    exit_coord: tuple[int, int],
    path: list[str],
    show_path: bool = True,
) -> str:
    path_positions = {entry}
    x, y = entry
    direction_deltas = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }
    for direction in path:
        dx, dy = direction_deltas[direction]
        x += dx
        y += dy
        path_positions.add((x, y))
    lines: list[str] = []
    for y, row in enumerate(grid):
        top_line = ""
        for cell in row:
            if cell.is_open("N"):
                top_line += "+   "
            else:
                top_line += "+---"
        top_line += "+"
        lines.append(top_line)
        middle_line = ""
        for x, cell in enumerate(row):
            if cell.is_open("W"):
                middle_line += " "
            else:
                middle_line += "|"
            position = (x, y)
            if position == entry:
                middle_line += " E "
            elif position == exit_coord:
                middle_line += " X "
            elif show_path and position in path_positions:
                middle_line += " . "
            else:
                middle_line += "   "
        if row[-1].is_open("E"):
            middle_line += " "
        else:
            middle_line += "|"
        lines.append(middle_line)
    bottom_line = ""
    for cell in grid[-1]:
        bottom_line += "+"
        if cell.is_open("S"):
            bottom_line += "   "
        else:
            bottom_line += "---"
    bottom_line += "+"
    lines.append(bottom_line)
    return "\n".join(lines) + "\n"
