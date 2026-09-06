import sys
from cli.config_parser import parse_config
from cli.errors import ConfigError

def main() -> int:
	if len(sys.argv) != 2:
		print("Usage: python3 a_maze_ing.py config.txt")
		return 1
	try:
		config = parse_config(sys.argv[1])
	except FileNotFoundError:
		print(f"Error: configuration file not found: {sys.argv[1]}")
		return 1
	print(f"Maze size: {config.width} x {config.height}")
	print(f"Entry: {config.entry}")
	print(f"Exit: {config.exit}")
	print(f"Perfect mode: {config.perfect}")
	return 0

if __name__ == "__main__":
	raise SystemExit(main())