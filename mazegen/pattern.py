def pattern_rows() -> tuple[str, ...]:
    digit_4 = ("X..", "X..", "XXX", "..X", "..X")
    digit_2 = ("XXX", "..X", "XXX", "X..", "XXX")
    return tuple(left + "." + right for left, right in zip(digit_4, digit_2))


def minimum_size() -> tuple[int, int]:
    rows = pattern_rows()
    return len(rows[0]) + 2, len(rows) + 2


def plan_pattern(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_coord: tuple[int, int],
) -> tuple[set[tuple[int, int]], str]:
    rows = pattern_rows()
    pattern_width = len(rows[0])
    pattern_height = len(rows)
    start_x = width // 2 - pattern_width // 2
    start_y = height // 2 - pattern_height // 2
    fits = (
        start_x >= 1
        and start_y >= 1
        and start_x + pattern_width <= width - 1
        and start_y + pattern_height <= height - 1
    )
    if not fits:
        min_width, min_height = minimum_size()
        return set(), (
            f"(minimum {min_width}x{min_height})."
        )
    cells = {
        (start_x + col, start_y + row)
        for row, line in enumerate(rows)
        for col, char in enumerate(line)
        if char == "X"
    }
    if entry in cells or exit_coord in cells:
        return set(), "Error: pattern 42 omitted, entry or exit is inside it."
    return cells, ""
