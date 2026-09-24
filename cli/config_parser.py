from dataclasses import dataclass
from mazegen.generator import MazeGenerator
from .errors import ConfigError


@dataclass
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    algorithm: str = "dfs"


def parse_bool(value: str, key: str = "PERFECT") -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ConfigError(f"{key} must be True or False.")


def parse_int(value: str, key: str) -> int:
    try:
        return int(value.strip())
    except ValueError as error:
        raise ConfigError(f"{key} must be an integer.") from error


def parse_positive_int(value: str, key: str) -> int:
    number = parse_int(value, key)
    if number <= 0:
        raise ConfigError(f"{key} must be greater than zero.")
    return number


def parse_coordinates(value: str, key: str) -> tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must use the format x,y.")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError as error:
        raise ConfigError(f"{key} coordinates must be integers.") from error


def parse_algorithm(value: str) -> str:
    algorithm = value.strip().lower()
    if algorithm not in MazeGenerator.ALGORITHMS:
        raise ConfigError(
            "ALGORITHM must be one of: "
            + ", ".join(MazeGenerator.ALGORITHMS) + "."
        )
    return algorithm


def check_inside_maze(
    name: str,
    coordinate: tuple[int, int],
    width: int,
    height: int,
) -> None:
    x, y = coordinate
    if not (0 <= x < width and 0 <= y < height):
        raise ConfigError(
            f"{name} coordinate {coordinate} is outside the maze bounds."
        )


def read_key_values(path: str) -> dict[str, str]:
    try:
        with open(path, "r", encoding="utf-8") as config_file:
            lines = config_file.read().splitlines()
    except FileNotFoundError:
        raise
    except (OSError, UnicodeDecodeError) as error:
        raise ConfigError(
            f"Cannot read configuration file '{path}': {error}"
        ) from error
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(
                f"Line {line_number} must use the format KEY=VALUE."
            )
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ConfigError(f"Line {line_number} has an empty key.")
        if not value:
            raise ConfigError(f"Line {line_number} has an empty value.")
        if key in values:
            raise ConfigError(
                f"Line {line_number} duplicate configuration key: {key}."
            )
        values[key] = value
    return values


def check_required_keys(values: dict[str, str]) -> None:
    required_keys = (
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    )
    missing = [key for key in required_keys if key not in values]
    if missing:
        raise ConfigError(
            "Missing required configuration keys: " + ", ".join(missing) + "."
        )


def parse_config(path: str) -> MazeConfig:
    values = read_key_values(path)
    check_required_keys(values)
    width = parse_positive_int(values["WIDTH"], "WIDTH")
    height = parse_positive_int(values["HEIGHT"], "HEIGHT")
    entry = parse_coordinates(values["ENTRY"], "ENTRY")
    exit_coordinate = parse_coordinates(values["EXIT"], "EXIT")
    check_inside_maze("ENTRY", entry, width, height)
    check_inside_maze("EXIT", exit_coordinate, width, height)
    if entry == exit_coordinate:
        raise ConfigError("ENTRY and EXIT must be different.")
    seed = None
    if "SEED" in values:
        seed = parse_int(values["SEED"], "SEED")
    algorithm = "dfs"
    if "ALGORITHM" in values:
        algorithm = parse_algorithm(values["ALGORITHM"])
    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coordinate,
        output_file=values["OUTPUT_FILE"],
        perfect=parse_bool(values["PERFECT"]),
        seed=seed,
        algorithm=algorithm,
    )
