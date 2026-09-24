from mazegen.generator import Cell, MazeGenerator
from dataclasses import dataclass
from cli.config_parser import MazeConfig
from mazegen.solver import MazeSolver
from mazegen.encoder import encode_maze, write_file


@dataclass
class MazeState:
    grid: list[list[Cell]]
    path: list[str]
    pattern_cells: set[tuple[int, int]]


def state_from_grid(
    config: MazeConfig,
    generator: MazeGenerator,
    grid: list[list[Cell]],
) -> MazeState:
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


def make_generator(config: MazeConfig, seed: int | None) -> MazeGenerator:
    return MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_coord=config.exit,
        perfect=config.perfect,
        seed=seed,
        algorithm=config.algorithm,
    )


def build_maze(config: MazeConfig, seed: int | None) -> MazeState:
    generator = make_generator(config, seed)
    return state_from_grid(config, generator, generator.generate())


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

