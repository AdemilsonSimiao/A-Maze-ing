from cli.config_parser import MazeConfig
from app.session import MazeState, save_maze
from app.animation import render_maze, animate_path, animate_maze


def read_choice() -> str:
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show / Hide the shortest path")
    print("3. Rotate the wall colours")
    print("4. Quit")
    return input("Choice? (1-4): ").strip()


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


def run_menu(config: MazeConfig, state: MazeState) -> None:
    colors = wall_colors()
    color_index = 0
    show_path = True
    message = ""
    clear_screen = "\033[H\033[2J\033[3J"
    while True:
        print(clear_screen, end="")
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
            print(clear_screen, end="")
            state = animate_maze(config, None, colors[color_index])
            save_maze(config, state)
            print(clear_screen, end="")
            animate_path(config, state, colors[color_index])
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(colors)
        elif choice == "4":
            return
        else:
            message = "Invalid choice. Please enter a number from 1 to 4."
