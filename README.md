<div align="center">

## Zippy

**Multi-purpose archive extraction, repair and brute-force toolkit.**

![PyPI](https://img.shields.io/pypi/v/py-zippy?color=blue&logo=pypi&style=flat-square) ![Python](https://img.shields.io/pypi/pyversions/py-zippy?color=blue&logo=python&style=flat-square) ![License](https://img.shields.io/pypi/l/py-zippy?color=blue&logo=apache&style=flat-square)

**Broad format coverage** - (`tar`, `tar.gz`, `tar.bz2`, `tar.xz`, `tar.lzma`), (`gzip`, `bz2`, `xz`, `lzma`), (`7z`, `rar`, `zstd`)

**Consistent UX** - consistent logging, progress indicators, and tab completion for every command.

**Security tooling** - create or re-lock encrypted ZIPs, run smart dictionary attacks with a password list

**Integrity & repair** - repair, attempt salvage extractions, and perform best-effort recovery.
</div>


## Installation

### From PyPI (recommended)

```bash
python -m pip install zippy
```

### From source

```bash
git clone https://github.com/John0n1/ZIPPY.git
cd ZIPPY
python -m pip install .

### Debian package

```bash
sudo apt install ./zippy_*.deb
```

## Quick start

```bash
# Extract an archive
zippy --extract backups/site.tar.xz -o ./site

# Create a password-protected ZIP from multiple paths
zippy --lock secure.zip -f docs,images -p "Tru5ted!"

# List TAR.BZ2 contents
zippy --list datasets.tar.bz2

# Attempt unlocking with the bundled wordlist
zippy --unlock encrypted.zip -d password_list.txt --verbose

# Run salvage repair on a damaged tarball
zippy --repair broken.tar.gz --repair-mode remove_corrupted
```

Run `zippy --help` for the full command reference or `zippy --version` to confirm the installed release.

## Supported archive formats

| Family | Types |
| ------ | ----- |
| ZIP | `zip` (with optional password protection) |
| TAR | `tar`, `tar.gz`, `tar.bz2`, `tar.xz`, `tar.lzma`, `.tgz`, `.tbz`, `.txz`, `.tlz` |
| Single-file | `gzip` (`.gz`), `bz2` (`.bz2`), `xz` (`.xz`), `lzma` (`.lzma`) |

Unsupported formats (e.g. 7z, rar, zstd) will raise a friendly error instructing you to choose a supported type.

## Configuration & automation

- Use `--save-config <file>` to capture the current flag set (including passwords or dictionary paths if provided).
- Rehydrate saved flags via `--load-config <file>` for repeatable batch jobs.
- Disable animations with `--no-animation` for CI environments.

## Logging & colours

Logging defaults to concise `INFO` output. Add `--verbose` for `DEBUG` traces. Colour output automatically downgrades in non-interactive terminals, while animations fall back to plain log messages when disabled or redirected. Windows terminals are supported through `colorama`.

## Password dictionary

The bundled `password_list.txt` contains hundreds of common credentials, curated for demonstration purposes. The unlock command trims duplicates, ignores comments (`# ...`), and safely handles mixed encodings. Supply your own list with `--dictionary <file>` for larger attacks.

## Contributing
Pull requests are welcome—please open an issue describing the enhancement before submitting substantial changes.

## License

Zippy is released under the MIT License. See `LICENSE` for the full text.

## Disclaimer

Zippy is provided "as is" without warranty of any kind. Use at your own risk and keep backups of critical data.

**The author is not responsible for any data loss or damage resulting from the use of this software.**
