from __future__ import annotations

import sys
from typing import Any

import tomlkit
from tomlkit.toml_document import TOMLDocument

from adsctl.utils.fs import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def save_toml_document(document: TOMLDocument, path: Path):
    path.ensure_parent_dir_exists()
    path.write_atomic(tomlkit.dumps(document), 'w', encoding='utf-8')


def create_toml_document(config: dict) -> TOMLDocument:
    return tomlkit.item(config)


def load_toml_data(data: str) -> dict[str, Any]:
    return tomllib.loads(data)


def load_toml_file(path: str) -> dict[str, Any]:
    with open(path, encoding='utf-8') as f:
        return tomllib.loads(f.read())
