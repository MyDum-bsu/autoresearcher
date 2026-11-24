"""Read explicit offline input; emit only after complete validation, to stdout."""

import argparse
import sys
from pathlib import Path

from pilot.checkers.finite_bellman import CheckerError
from pilot.science.contracts import ContractError, canonical, parse
from pilot.science.packet import build, markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--format", required=True, choices=("json", "markdown"))
    args = parser.parse_args()
    try:
        packet = build(parse(args.input.read_text(encoding="utf-8")))
        output = canonical(packet) + "\n" if args.format == "json" else markdown(packet)
    except (ContractError, CheckerError, OSError, UnicodeError) as error:
        print(f"offline dossier rejected: {error}", file=sys.stderr)
        return 2
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
