import os
import pathlib

_SIZES = ("small", "medium", "large")
_FORMATS = ("xml", "json", "yaml", "toml")


def fixtures_dir() -> pathlib.Path:
    env = os.environ.get("SERIALBENCH_FIXTURES")
    if env:
        return pathlib.Path(env)
    for candidate in (pathlib.Path("fixtures"), pathlib.Path("test_data")):
        if (candidate / "small.xml").exists():
            return candidate
    raise FileNotFoundError(
        "canonical fixtures not found: set SERIALBENCH_FIXTURES or clone "
        "https://github.com/serialbench/fixtures to ./fixtures"
    )


def artifact(name: str) -> str:
    return (fixtures_dir() / name).read_text()


def load(formats, sizes):
    base = fixtures_dir()
    return {
        size: {fmt: (base / f"{size}.{fmt}").read_bytes() if fmt == "cbor" else (base / f"{size}.{fmt}").read_text() for fmt in formats}
        for size in sizes
    }
