import time
from cli.config_parser import MazeConfig
from .session import MazeState, state_from_grid, make_generator
from display.ascii_renderer import render_maze


def frame_stride(total_cells: int, max_frames: int = 60) -> int:
    return max(1, total_cells // max_frames)


def animate_maze(
    config: MazeConfig,
    seed: int | None,
    wall_color: str,
) -> MazeState:
    clear_screen = "\033[H"
    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"
    print("\033[2J", end="")
    print(hide_cursor, end="")
    step_delay = 0.03
    generator = make_generator(config, seed)
    stride = frame_stride(config.width * config.height)
    step_iterator = generator.generate_steps()
    final_grid = None
    try:
        for index, grid in enumerate(step_iterator):
            final_grid = grid
            if index % stride != 0:
                continue
            print(clear_screen, end="")
            print(
                render_maze(
                    grid=grid,
                    entry=config.entry,
                    exit_coord=config.exit,
                    path=[],
                    show_path=False,
                    pattern_cells=generator.pattern_cells,
                    wall_color=wall_color,
                    colored=True,
                ),
                end="",
            )
            time.sleep(step_delay)
    except KeyboardInterrupt:
        print()
        for grid in step_iterator:
            final_grid = grid
    assert final_grid is not None
    print(clear_screen, end="")
    print(
        render_maze(
            grid=final_grid,
            entry=config.entry,
            exit_coord=config.exit,
            path=[],
            show_path=False,
            pattern_cells=generator.pattern_cells,
            wall_color=wall_color,
            colored=True,
        ),
        end="",
    )
    print(show_cursor, end="")
    return state_from_grid(config, generator, final_grid)


def animate_path(
    config: MazeConfig,
    state: MazeState,
    wall_color: str,
) -> None:
    clear_screen = "\033[H"
    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"
    print(hide_cursor, end="")
    step_delay = 0.05
    try:
        for step_count in range(len(state.path) + 1):
            print(clear_screen, end="")
            print(
                render_maze(
                    grid=state.grid,
                    entry=config.entry,
                    exit_coord=config.exit,
                    path=state.path[:step_count],
                    show_path=True,
                    pattern_cells=state.pattern_cells,
                    wall_color=wall_color,
                    colored=True,
                ),
                end="",
            )
            time.sleep(step_delay)
    except KeyboardInterrupt:
        print()
