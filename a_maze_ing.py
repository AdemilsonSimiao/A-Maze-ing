import sys
from dataclasses import dataclass
from cli.config_parser import MazeConfig, parse_config
from cli.errors import ConfigError
from display.ascii_renderer import render_maze
from mazegen.encoder import encode_maze, write_file
from mazegen.generator import Cell, MazeGenerator
from mazegen.solver import MazeSolver


@dataclass
class MazeState:
    grid: list[list[Cell]]
    path: list[str]
    pattern_cells: set[tuple[int, int]]


def load_config(config_path: str) -> MazeConfig | None:
    try:
        return parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: configuration file not found: {config_path}")
    except ConfigError as error:
        print(f"Error: {error}")
    return None


def build_maze(config: MazeConfig, seed: int | None) -> MazeState:
    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_coord=config.exit,
        perfect=config.perfect,
        seed=seed,
    )
    grid = generator.generate()
    solver = MazeSolver(
        grid=grid,
        entry=config.entry,
        exit_coord=config.exit,
    )
    return MazeState(
        grid=grid,
        path=solver.solve(),
        pattern_cells=generator.pattern_cells,
    )


def save_maze(config: MazeConfig, state: MazeState) -> bool:
    encoded_maze = encode_maze(
        grid=state.grid,
        entry=config.entry,
        exit_coord=config.exit,
        path=state.path,
    )
    try:
        write_file(config.output_file, encoded_maze)
    except OSError as error:
        print(f"Error: cannot write '{config.output_file}': {error}")
        return False
    return True


def display_maze(
    config: MazeConfig,
    state: MazeState,
    show_path: bool,
    wall_color: str,
) -> None:
    print(
        render_maze(
            grid=state.grid,
            entry=config.entry,
            exit_coord=config.exit,
            path=state.path,
            show_path=show_path,
            pattern_cells=state.pattern_cells,
            wall_color=wall_color,
            colored=True,
        ),
        end="",
    )


def wall_colors() -> tuple[str, ...]:
    return (
        "",
        "\033[31m",
        "\033[32m",
        "\033[33m",
        "\033[34m",
        "\033[35m",
        "\033[36m",
    )


def read_choice() -> str:
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show / Hide the shortest path")
    print("3. Rotate the wall colours")
    print("4. Quit")
    return input("Choice? (1-4): ").strip()


def run_menu(config: MazeConfig, state: MazeState) -> None:
    colors = wall_colors()
    color_index = 0
    show_path = True
    message = ""
    while True:
        display_maze(config, state, show_path, colors[color_index])
        if message:
            print(message)
            message = ""
        try:
            choice = read_choice()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if choice == "1":
            state = build_maze(config, None)
            save_maze(config, state)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(colors)
        elif choice == "4":
            return
        else:
            message = "Invalid choice. Please enter a number from 1 to 4."


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1
    config = load_config(sys.argv[1])
    if config is None:
        return 1
    state = build_maze(config, config.seed)
    if not save_maze(config, state):
        return 1
    run_menu(config, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
