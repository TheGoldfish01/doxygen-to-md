"""Simple CLI for doxygen_to_md"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from . import convert


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="doxygen-to-md", description="Convert Doxygen comments to Markdown"
    )
    parser.add_argument("infile", nargs="?", help="Input file (defaults to stdin)")
    parser.add_argument(
        "--outdir",
        "-o",
        help="Output directory to write Markdown files when infile is a directory",
    )
    args = parser.parse_args(argv)

    if args.infile:
        path = Path(args.infile)
        if path.is_dir():
            outdir = Path(args.outdir or "./doxygen_md_output")
            outdir.mkdir(parents=True, exist_ok=True)
            # process each XML file in directory
            for xml_file in sorted(path.glob("*.xml")):
                text = xml_file.read_text(encoding="utf-8")
                try:
                    md = convert(text)
                except ValueError as e:
                    print(
                        f"Skipping {xml_file.name}: not valid Doxygen XML ({e})",
                        file=sys.stderr,
                    )
                    continue
                # determine namespace/module for grouping
                try:
                    root = ET.fromstring(text)
                    comp = root.find("compounddef")
                    compname = (
                        comp.findtext("compoundname") if comp is not None else ""
                    ) or ""
                    compname = compname.strip()
                    kind = comp.get("kind", "") if comp is not None else ""
                except Exception:
                    compname = ""
                    kind = ""

                if kind == "namespace" and compname:
                    group = compname
                elif "::" in compname:
                    group = compname.split("::")[0]
                else:
                    group = "global"

                group_dir = outdir.joinpath(group)
                group_dir.mkdir(parents=True, exist_ok=True)

                out_file = group_dir.joinpath(xml_file.stem + ".md")
                out_file.write_text(md, encoding="utf-8")
                print(f"Wrote {out_file}")
            return 0
        else:
            text = path.read_text(encoding="utf-8")
            md = convert(text)
            print(md)
            return 0
    else:
        text = sys.stdin.read()
        md = convert(text)
        print(md)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
