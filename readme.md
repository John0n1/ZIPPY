git clone https://github.com/John0n1/zippy.git
<div align="center">

# Zippy Toolkit

**Multi-format archive automation with colourised logging, password workflows, and repair tooling.**

</div>

- **Broad format coverage** - ZIP family (including APK/JAR/WAR/IPA/EAR), TAR variants (`tar`, `tar.gz`, `tar.bz2`, `tar.xz`, `tar.lzma`) and single-file compressors (`gzip`, `bz2`, `xz`, `lzma`).
- **Consistent UX** - colour-aware logging, animated progress indicators, and tab completion for every command.
- **Security tooling** - create or re-lock encrypted ZIPs, run smart dictionary attacks with the bundled password list, and capture verbose traces when needed.
- **Integrity & repair** - smoke-test archives, attempt salvage extractions, and perform best-effort recovery for TAR and single-file formats.
- **Packaging ready** - modern `pyproject.toml`, Debian packaging assets, and best-practice metadata for distribution.

## Installation

### From PyPI (recommended)

```bash
python -m pip install py-zippy
```

### From source

```bash
git clone https://github.com/John0n1/ZIPPY.git
cd ZIPPY
python -m pip install .
```

### Debian package build

```bash
dpkg-buildpackage -us -uc
sudo dpkg -i ../zippy_*_all.deb
```

## Quick start

```bash
# Extract an archive
zippy extract backups/site.tar.xz -o ./site

# Create a password-protected ZIP from multiple paths
zippy lock secure.zip -f docs,images -p "Tru5ted!"

# List TAR.BZ2 contents
zippy list datasets.tar.bz2

# Attempt unlocking with the bundled wordlist
zippy unlock encrypted.zip -d password_list.txt --verbose

# Run salvage repair on a damaged tarball
zippy repair broken.tar.gz --repair-mode remove_corrupted
```

Run `zippy help` for the full command reference or `zippy --version` to confirm the installed release.

## Supported archive formats

| Family | Types |
| ------ | ----- |
| ZIP family | `zip`, `jar`, `war`, `ear`, `apk`, `ipa` (AES encryption supported via `pyzipper`) |
| TAR family | `tar`, `tar.gz`, `tar.bz2`, `tar.xz`, `tar.lzma`, `.tgz`, `.tbz`, `.txz`, `.tlz` |
| Single-file | `gzip` (`.gz`), `bz2` (`.bz2`), `xz` (`.xz`), `lzma` (`.lzma`) |
| External (via `patool`) | `rar`, `7z`, `zst`, `tar.zst`, `tar.lz`, `lz`, `cab`, `iso`, `img`, `sit`, `sitx`, `hqx`, `arj`, `lzh`, `ace`, `z`, `Z`, `cpio`, `deb`, `rpm`, `pkg`, `xar`, `appimage` |

External formats require the optional [`patool`](https://wummel.github.io/patool/) package and the corresponding backend binaries (e.g. `unrar`, `7z`, `cabextract`). Zippy detects missing tools and guides you through resolving them.

## Configuration & automation

- Use `--save-config <file>` to capture the current flag set (including passwords or dictionary paths if provided).
- Rehydrate saved flags via `--load-config <file>` for repeatable batch jobs.
- Disable animations with `--no-animation` for CI environments.

## Logging & colours

Logging defaults to concise `INFO` output. Add `--verbose` for `DEBUG` traces. Colour output automatically downgrades in non-interactive terminals, while animations fall back to plain log messages when disabled or redirected. Windows terminals are supported through `colorama`.

## Password dictionary

The bundled `password_list.txt` contains hundreds of common credentials, curated for demonstration purposes. The unlock command trims duplicates, ignores comments (`# ...`), and safely handles mixed encodings. Supply your own list with `--dictionary <file>` for larger attacks.

## Development

```bash
python -m pip install -r requirements.txt
python -m pip install -e .[dev]  # if you add optional tooling

# Lint / type-check (examples)
ruff check
pyright
```

Pull requests are welcome—please open an issue describing the enhancement before submitting substantial changes.

## License

Zippy is released under the MIT License. See `LICENSE` for the full text.

## Disclaimer

Zippy is provided "as is" without warranty of any kind. Use at your own risk and keep backups of critical data.



