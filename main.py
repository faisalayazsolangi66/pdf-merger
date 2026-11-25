#!/usr/bin/env python3
"""Merge several PDF files into one.

Appends the pages of each input PDF, in the order given, into a
single output PDF using pypdf. Encrypted or unreadable inputs are
reported and skipped only when ``--skip-errors`` is set; otherwise
the merge stops with an error.
"""
import argparse
import os
import sys

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:  # pragma: no cover - handled with a clear message
    PdfReader = PdfWriter = None


def merge(inputs, output, skip_errors=False):
    """Merge *inputs* into *output*; return the total page count."""
    writer = PdfWriter()
    total_pages = 0
    for path in inputs:
        try:
            reader = PdfReader(path)
            if reader.is_encrypted:
                raise ValueError("file is encrypted")
            for page in reader.pages:
                writer.add_page(page)
            print(f"  added {path} ({len(reader.pages)} page(s))")
            total_pages += len(reader.pages)
        except Exception as exc:
            if skip_errors:
                print(f"  skipped {path}: {exc}", file=sys.stderr)
                continue
            raise ValueError(f"{path}: {exc}") from exc
    if total_pages == 0:
        raise ValueError("no pages were added; nothing to write")
    with open(output, "wb") as handle:
        writer.write(handle)
    return total_pages


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Merge several PDF files into one.")
    parser.add_argument("inputs", nargs="+", metavar="PDF",
                        help="input PDF files, in merge order")
    parser.add_argument("-o", "--output", required=True,
                        help="output PDF file")
    parser.add_argument("--overwrite", action="store_true",
                        help="overwrite the output file if it exists")
    parser.add_argument("--skip-errors", action="store_true",
                        help="skip unreadable inputs instead of stopping")
    args = parser.parse_args(argv)

    if PdfReader is None:
        print("error: pypdf is not installed. Run: pip install -r "
              "requirements.txt", file=sys.stderr)
        return 1
    for path in args.inputs:
        if not os.path.isfile(path):
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
    if os.path.exists(args.output) and not args.overwrite:
        print(f"error: output already exists: {args.output} "
              f"(use --overwrite)", file=sys.stderr)
        return 1
    if len(args.inputs) < 2:
        print("warning: only one input PDF given")

    print(f"Merging {len(args.inputs)} PDF(s) into {args.output} ...")
    try:
        pages = merge(args.inputs, args.output,
                      skip_errors=args.skip_errors)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Done: {args.output} ({pages} page(s) from "
          f"{len(args.inputs)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
