from dataclasses import dataclass
from .errors import ConfigError

@dataclass
class MazeConfig:
	width: int
	height: int
	entry: tuple[int , int]
	exit: tuple[int, int]
	output_file: str
	perfect: bool
	seed: int | None = None

def parse_bool(value: str) -> bool:
	normalized = value.strip().lower()
	if normalized == "true":
		return True
	if normalized == "false":
			return False
	raise ConfigError("PERFECT must be True or False.")

def parse_coordinates(value: str, key: str) -> tuple[int, int]:
	parts = value.split(",")
	if len(parts) != 2:
		raise ConfigError(f"{key} must use the format x,y")
	try:
		return int(parts[0].strip()), int(parts[1].strip())
	except ValueError as error:
		raise ConfigError(f"{key} coordinates must be integer.")

def parse_config(path: str) -> MazeConfig:
	values: dict[str, str] = {}
	with open(path, "r", encoding="utf-8") as config_file:
		for line_number, raw_line in enumerate(config_file, start=1):
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
				raise ValueError(f"Line {line_number} has an empty key.")
			if not value:
							raise ValueError(f"Line {line_number} has an empty value.")
			if key in values:
				raise ValueError(f"Duplicate configuration key: {key}.")
			values[key] = value
		required_keys = {
			"WIDTH",
			"HEIGHT",
			"ENTRY",
			"EXIT",
			"OUTPUT_FILE",
			"PERFECT",
			"SEED",
		}
		missing_keys = required_keys - values.keys()
		if missing_keys:
			missing = ", ".join(sorted(missing_keys))
			raise ConfigError(f"Missing required configuration keys: {missing}.")
		try:
			width = int(values["WIDTH"])
			height = int(values["HEIGHT"])
		except ValueError as error:
			raise ConfigError("WIDTH and HEIGHT must be greater than zero.")
		entry = parse_coordinates(values["ENTRY"], "ENTRY")
		exit_coordinate = parse_coordinates(values["EXIT"], "EXIT")
		for name, coordinate in (
			("ENTRY", entry),
			("EXIT", exit_coordinate),
		):
			x, y = coordinate
			if not (0 <= x < width and 0 <= y < height):
				raise ConfigError(
					f"{name} coordinate {coordinate} is outside the maze bounds."
				)
			if entry == exit_coordinate:
				raise ConfigError("ENTRY and EXIT must be different.")
		output_file = values["OUTPUT_FILE"]
		perfect = parse_bool(values["PERFECT"])
		seed: int | None = None
		if "SEED" in values:
			try:
				seed = int(values["SEED"])
			except ValueError as error:
				raise ConfigError("SEED must be an interger.") from error
		return MazeConfig(
			width=width,
			height=height,
			entry=entry,
			exit=exit_coordinate,
			output_file=output_file,
			perfect=perfect,
			seed=seed,
		)