import sys
from cli.config_parser import MazeConfig, parse_config
from cli.errors import ConfigError
from app.animation import animate_maze, animate_path
from app.menu import run_menu, wall_colors
from app.session import save_maze


def load_config(config_path: str) -> MazeConfig | None:
    try:
        return parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: configuration file not found: {config_path}")
    except ConfigError as error:
        print(f"Error: {error}")
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1
    config = load_config(sys.argv[1])
    if config is None:
        return 1
    clear_screen = "\033[H\033[2J\033[3J"
    print(clear_screen, end="")
    state = animate_maze(config, config.seed, wall_colors()[0])
    if not save_maze(config, state):
        return 1
    animate_path(config, state, wall_colors()[0])
    print(clear_screen, end="")
    run_menu(config, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
