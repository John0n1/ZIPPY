# ZIPsnipp - Your Swiss Army Knife for Archive Files
```
▗▄▄▄▄▖▗▄▄▄▖▗▄▄▖  ▗▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖ ▗▄▄▖ 
   ▗▞▘  █  ▐▌ ▐▌▐▌   ▐▛▚▖▐▌  █  ▐▌ ▐▌▐▌ ▐▌
 ▗▞▘    █  ▐▛▀▘  ▝▀▚▖▐▌ ▝▜▌  █  ▐▛▀▘ ▐▛▀▘ 
▐▙▄▄▄▖▗▄█▄▖▐▌   ▗▄▄▞▘▐▌  ▐▌▗▄█▄▖▐▌   ▐▌   
```

ZIPsnipp is a command-line utility written in Python designed to be your comprehensive toolkit for handling various archive file formats. It aims to provide a user-friendly and powerful interface for common archive operations, including extraction, creation, listing, testing, password management, and even experimental repair and salvage capabilities.

## Features

* **Extract Archives**: Easily extract the contents of `.zip`, `.tar`, `.tar.gz`, `.tgz`, and `.gz` archives
* **Create Archives**: Generate new `.zip`, `.tar`, `.tar.gz`, and `.gz` archives from files and directories
* **List Archive Contents**: Quickly view the files and directories within an archive
* **Test Archive Integrity**: Check for errors and corruption in your archive files
* **Unlock Password-Protected ZIPs**: Attempt to crack password-protected ZIP archives using dictionary attacks
* **Lock Archives (ZIP)**: Create password-protected `.zip` archives and add files during the locking process
* **Experimental Archive Repair**: Includes experimental features to attempt repair of corrupted `.zip` and `.tar` archives, and basic salvage for `.gzip`
  * **ZIP Repair Modes**:
    * `remove_corrupted` (default): Attempts to remove corrupted files from ZIP archives
    * `scan_only`: Only scans and reports corrupted files in ZIP archives without repair actions
  * **Salvage Extraction**: Even if repair fails, ZIPsnipp attempts to extract any salvageable content from corrupted archives
* **User-Friendly CLI**: Clean and intuitive command-line interface with options and help messages
* **Loading Animation**: Provides visual feedback during operations (can be disabled)
* **Verbose Output**: Option for detailed output for debugging and advanced users

## Supported Archive Types

* `.zip`
* `.tar`
* `.tar.gz` (`.tgz`)
* `.gz` (gzip compressed single files)

## Installation

1. **Prerequisites**: Ensure you have Python 3.x installed on your system
2. **Download ZIPsnipp**: Download the `ZIPsnipp.py` script from this repository
3. **Make Executable (Linux/macOS)**:
    ```bash
    chmod +x ZIPsnipp.py
    ```
4. **Run from anywhere (Optional - Linux/macOS)**: Place `ZIPsnipp.py` in a directory in your system's `PATH` (e.g., `/usr/local/bin/`) to run it directly as `ZIPsnipp` from any terminal location

## Usage

Run ZIPsnipp from your terminal using the following command structure:

```bash
./ZIPsnipp.py <command> [archive_file] [options]
```

### Available Commands

* `extract`: Extract archive contents
* `create`: Create a new archive
* `list`: List contents of an archive
* `test`: Test archive integrity
* `unlock`: Attempt to unlock a password-protected archive
* `lock`: Create a password-protected archive (and add files)
* `repair`: [Experimental] Attempt to repair a corrupted archive
* `help`: Display help message
* `version`: Show script version

### Examples

```bash
# Extract a ZIP archive
./ZIPsnipp.py extract myarchive.zip

# Extract to specific directory
./ZIPsnipp.py extract myarchive.tar.gz -o extracted_files

# Create ZIP archive
./ZIPsnipp.py create new_archive.zip -f file1.txt,directory1,image.jpg

# Create password-protected ZIP
./ZIPsnipp.py lock secure_archive.zip -f important_documents,photos -p MySecretPassword

# Unlock password-protected ZIP
./ZIPsnipp.py unlock protected.zip -d passwords.txt

# Repair corrupted ZIP
./ZIPsnipp.py repair corrupted.zip --repair-mode remove_corrupted

# List contents
./ZIPsnipp.py list myarchive.tar

# Test integrity
./ZIPsnipp.py test archive_to_test.zip

# Show help
./ZIPsnipp.py help

# Show version
./ZIPsnipp.py version
```

### Options

| Option | Short | Description | Commands |
|--------|-------|-------------|----------|
| `--output <path>` | `-o` | Output directory for extraction | `extract` |
| `--password <password>` | `-p` | Password for operations | `extract`, `lock`, `unlock` |
| `--dictionary <file>` | `-d` | Dictionary file for password cracking | `unlock` |
| `--files <file1,file2,...>` | `-f` | Files to add | `create`, `lock` |
| `--type <type>` | | Force archive type | `create`, `lock` |
| `--repair-mode <mode>` | | Repair mode for ZIP archives | `repair` |
| `--verbose` | | Enable verbose output | All |
| `--no-animation` | | Disable loading animation | All |

## Notes and Limitations

* Password dictionary required for unlock command
* Password recovery uses brute-force/dictionary attack
* Archive repair is experimental
* File paths in create/lock commands need comma separation
* Proper permissions required for operations

## License

[MIT License]

