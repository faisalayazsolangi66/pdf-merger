# PDF Merger

Merge several PDF files into one, using
[pypdf](https://pypdf.readthedocs.io/). Pages are appended in the
order the files are given on the command line. Encrypted or
unreadable inputs stop the merge, unless `--skip-errors` is set.

## Requirements

- Python 3
- pypdf (see `requirements.txt`)

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py chapter1.pdf chapter2.pdf -o book.pdf
python3 main.py a.pdf b.pdf c.pdf -o combined.pdf --overwrite
python3 main.py *.pdf -o all.pdf --skip-errors
```

## Example

```bash
$ python3 main.py chapter1.pdf chapter2.pdf -o book.pdf
Merging 2 PDF(s) into book.pdf ...
  added chapter1.pdf (4 page(s))
  added chapter2.pdf (6 page(s))
Done: book.pdf (10 page(s) from 2 file(s))
```

## License

MIT — see [LICENSE](LICENSE).
