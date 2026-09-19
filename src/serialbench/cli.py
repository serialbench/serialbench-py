import argparse
import pathlib
import sys

from .platform_info import detect, env_key
from .result import write
from .runner import run_format
from .test_data import load


def main(argv=None):
    parser = argparse.ArgumentParser(prog="serialbench", description="Python serialization benchmarks on canonical fixtures")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="benchmark one format")
    run.add_argument("--format", required=True, choices=["xml", "json", "yaml", "toml", "cbor"])
    run.add_argument("--platform-name", required=True, help="runner platform label, e.g. macos-26")
    run.add_argument("--out", required=True, help="output results.yaml path")
    args = parser.parse_args(argv)

    data = load([args.format], ["small", "medium", "large"])
    print(f"serialbench-py | {args.format} | {env_key(args.platform_name)}")
    result = run_format(args.format, data)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, args.format, detect(args.platform_name), result, benchmark_name=f"py-full-{args.format}")
    print(f"results: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
