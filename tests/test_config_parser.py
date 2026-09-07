import unittest
import tempfile
from pathlib import Path

from cli.config_parser import parse_config
from cli.errors import ConfigError

class TestConfigParser(unittest.TestCase):
    def create_config(self, content: str) -> str:
        temp_folder = tempfile.TemporaryDirectory()
        self.addClassCleanup(temp_folder.cleanup)
        config_path = Path(temp_folder.name) / "config.txt"
        config_path.write_text(content, encoding="utf-8")
        return str(config_path)

    def test_valid_config(self) -> None:
        config_path = self.create_config(
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
            "SEED=42\n"
        )
        config = parse_config(config_path)
        self.assertEqual(config.width, 20)
        self.assertEqual(config.height, 15)
        self.assertEqual(config.entry, (0, 0))
        self.assertEqual(config.exit, (19, 14))
        self.assertEqual(config.output_file, "maze.txt")
        self.assertEqual(config.perfect, True)
        self.assertEqual(config.seed, 42)

    def test_missing_required_key(self) -> None:
        config_path = self.create_config(
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
            "SEED=42\n"
        )
        with self.assertRaisesRegex(ConfigError, "Missing required"):
            parse_config(config_path)

    def test_exit_outside_bounds(self) -> None:
        config_path = self.create_config(
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=20,14\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
            "SEED=42\n"
        )
        with self.assertRaisesRegex(ConfigError, "outside the maze bounds"):
            parse_config(config_path)

    def test_entry_and_exit_must_differ(self) -> None:
        config_path = self.create_config(
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=0,0\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
            "SEED=42\n"
        )
        with self.assertRaisesRegex(ConfigError, "ENTRY and EXIT must be different"):
            parse_config(config_path)

if __name__ == "__main__":
    unittest.main()