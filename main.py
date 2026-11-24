#!/usr/bin/env python3
"""Worst AI Advice entry: write the graded one-liner to the output dir.

Pure Python stdlib. Writes the entry text (139 chars, no trailing
newline) to MAKEFUN_OUTPUT_DIR (default /output) first, then a
best-effort local copy next to this script.
"""

import os
import sys

ENTRY = (
    "Certainly! To dry a wet phone quickly, microwave it for 30 seconds "
    "\u2014 the waves evaporate the water and top up the battery at the "
    "same time."
)


def write_copy(path, data, make_dirs=False):
    """Write data to path with mode 0644; return True on success."""
    try:
        if make_dirs:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(path, 0o644)
        with open(path, "rb") as handle:
            if handle.read() != data:
                return False
        return True
    except OSError:
        return False


def main() -> int:
    data = ENTRY.encode("utf-8")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    graded_path = os.path.join(output_dir, "entry.txt")
    local_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.txt"
    )

    wrote = write_copy(graded_path, data, make_dirs=True)
    if not wrote:
        wrote = write_copy(local_path, data)
    else:
        write_copy(local_path, data)

    if not wrote:
        raise SystemExit("failed to write entry.txt anywhere")

    return 0


if __name__ == "__main__":
    sys.exit(main())
