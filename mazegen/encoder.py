from .generator import Cell


def encode_cell(cell: Cell) -> str:
    return format(cell.walls, "X")


def encode_grid(grid: list[list[Cell]]) -> list[str]:
    return ["".join(encode_cell(cell)for cell in row) for row in grid]


def encode_maze(
    grid: list[list[Cell]],
    entry: tuple[int, int],
    exit_coord: tuple[int, int],
    path: list[str],
) -> str:
    rows = encode_grid(grid)
    lines = [
        *rows,
        "",
        f"{entry[0]},{entry[1]}",
        f"{exit_coord[0]},{exit_coord[1]}",
        "".join(path),
    ]
    return "\n".join(lines) + "\n"


def write_file(out_path: str, encoded_maze: str) -> None:
    with open(out_path, "w", encoding="utf-8") as file:
        file.write(encoded_maze)
