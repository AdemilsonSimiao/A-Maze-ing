from mazegen.generator import Cell


def _paint(text: str, color: str) -> str:
    if not color:
        return text
    return f"{color}{text}\033[0m"


def _build_path_positions(
    entry: tuple[int, int],
    path: list[str],
) -> set[tuple[int, int]]:
    path_positions: set[tuple[int, int]] = {entry}
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
    return path_positions


def _horizon_line(
    row: list[Cell],
    direction: str,
    wall_color: str,
) -> str:
    line = ""
    for cell in row:
        line += _paint("+", wall_color)
        if cell.is_open(direction):
            line += "   "
        else:
            line += _paint("---", wall_color)
    return line + _paint("+", wall_color)


def _middle_line(
    row: list[Cell],
    y: int,
    contents: dict[tuple[int, int], str],
    wall_color: str,
) -> str:
    line = ""
    for x, cell in enumerate(row):
        if cell.is_open("W"):
            line += " "
        else:
            line += _paint("|", wall_color)
        line += contents.get((x, y), "   ")
    if row[-1].is_open("E"):
        line += " "
    else:
        line += _paint("|", wall_color)
    return line


def _build_contents(
    entry: tuple[int, int],
    exit_coord: tuple[int, int],
    path: list[str],
    show_path: bool,
    pattern_cells: set[tuple[int, int]],
    colored: bool,
) -> dict[tuple[int, int], str]:
    green = "\033[32m" if colored else ""
    red = "\033[31m" if colored else ""
    cyan = "\033[36m" if colored else ""
    white = "\033[37m" if colored else ""
    contents: dict[tuple[int, int], str] = {}
    if show_path:
        for position in _build_path_positions(entry, path):
            contents[position] = _paint(" . ", cyan)
    for position in pattern_cells:
        contents[position] = _paint("###", white)
    contents[entry] = _paint(" E ", green)
    contents[exit_coord] = _paint(" X ", red)
    return contents


def render_maze(
    grid: list[list[Cell]],
    entry: tuple[int, int],
    exit_coord: tuple[int, int],
    path: list[str],
    show_path: bool = True,
    pattern_cells: set[tuple[int, int]] | None = None,
    wall_color: str = "",
    colored: bool = False,
) -> str:
    contents = _build_contents(
        entry=entry,
        exit_coord=exit_coord,
        path=path,
        show_path=show_path,
        pattern_cells=pattern_cells or set(),
        colored=colored,
    )
    lines: list[str] = []
    for y, row in enumerate(grid):
        lines.append(_horizon_line(row, "N", wall_color))
        lines.append(_middle_line(row, y, contents, wall_color))
    lines.append(_horizon_line(grid[-1], "S", wall_color))
    return "\n".join(lines) + "\n"
