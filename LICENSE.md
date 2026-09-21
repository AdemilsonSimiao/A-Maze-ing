[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "mazegen"
version = "1.0.0"
description = "Reusable maze generator with a shortest-path solver and a hexadecimal encoder."
readme = "README.md"
requires-python = ">=3.10"
license-files = ["LICENSE.md"]

[tool.setuptools]
packages = ["mazegen"]

[tool.setuptools.package-data]
mazegen = ["py.typed"]