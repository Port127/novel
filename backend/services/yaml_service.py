from pathlib import Path
from ruamel.yaml import YAML

_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.default_flow_style = False
_yaml.allow_unicode = True
_yaml.width = 4096


def read_yaml(path: Path) -> dict:
    """Read a YAML file preserving comments. Returns empty dict if missing."""
    path = Path(path)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    data = _yaml.load(text)
    return dict(data) if data else {}


def write_yaml(path: Path, data) -> None:
    """Write data to a YAML file, preserving round-trip style when possible."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        _yaml.dump(data, f)


def read_markdown(path: Path) -> str:
    """Read a markdown file. Returns empty string if missing."""
    path = Path(path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    """Write content to a markdown file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
