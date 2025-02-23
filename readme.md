# Zippy

Zippy is a command-line utility written in Python designed for handling various archive file formats. It aims to provide a user-friendly interface for common archive operations, including extraction, creation, listing, testing, password management, and even experimental repair and salvage capabilities.

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
  * **Salvage Extraction**: Even if repair fails, Zippy attempts to extract any salvageable content from corrupted archives
* **User-Friendly CLI**: Clean and intuitive command-line interface with options and help messages
* **Loading Animation**: Provides visual feedback during operations (can be disabled)
* **Verbose Output**: Option for detailed output for debugging and advanced users
* **Interactive Prompts**: Prompts for missing arguments such as output directory and files to add
* **Configuration Management**: Save and load configurations for common operations
* **Environment Variables**: Support for environment variables to set default values for common options
* **Auto-Completion**: Auto-completion for commands and options

## Supported Archive Types

* `.zip`
* `.tar`
* `.tar.gz` (`.tgz`)
* `.gz` (gzip compressed single files)

## Installation

1. **Prerequisites**: Ensure you have Python 3.x installed on your system
2. **Download Zippy**: Download the `Zippy.py` script from this repository
3. **Make Executable (Linux/macOS)**:
    ```bash
    chmod +x Zippy.py
    ```
4. **Run from anywhere (Optional - Linux/macOS)**: Place `Zippy.py` in a directory in your system's `PATH` (e.g., `/usr/local/bin/`) to run it directly as `Zippy` from any terminal location

## Usage

Run Zippy from your terminal using the following command structure:

```bash
./Zippy.py <command> [archive_file] [options]
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
./Zippy.py extract myarchive.zip

# Extract to specific directory
./Zippy.py extract myarchive.tar.gz -o extracted_files

# Create ZIP archive
./Zippy.py create new_archive.zip -f file1.txt,directory1,image.jpg

# Create password-protected ZIP
./Zippy.py lock secure_archive.zip -f important_documents,photos -p MySecretPassword

# Unlock password-protected ZIP
./Zippy.py unlock protected.zip -d passwords.txt

# Repair corrupted ZIP
./Zippy.py repair corrupted.zip --repair-mode remove_corrupted

# List contents
./Zippy.py list myarchive.tar

# Test integrity
./Zippy.py test archive_to_test.zip

# Show help
./Zippy.py help

# Show version
./Zippy.py version
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
| `--save-config <file>` | | Save current settings to a configuration file | All |
| `--load-config <file>` | | Load settings from a configuration file | All |

## Quick Start Guide

1. **Extracting an Archive**:
    ```bash
    ./Zippy.py extract myarchive.zip
    ```

2. **Creating a New Archive**:
    ```bash
    ./Zippy.py create new_archive.zip -f file1.txt,directory1,image.jpg
    ```

3. **Creating a Password-Protected Archive**:
    ```bash
    ./Zippy.py lock secure_archive.zip -f important_documents,photos -p MySecretPassword
    ```

4. **Unlocking a Password-Protected Archive**:
    ```bash
    ./Zippy.py unlock protected.zip -d passwords.txt
    ```

5. **Repairing a Corrupted Archive**:
    ```bash
    ./Zippy.py repair corrupted.zip --repair-mode remove_corrupted
    ```

## Common Errors and Troubleshooting

1. **Error: Archive file not found**:
    * Ensure the archive file path is correct and the file exists.
    * Use absolute paths if relative paths are causing issues.

2. **Error: Unsupported archive type**:
    * Check if the archive type is supported by Zippy.
    * Use the `--type` option to specify the archive type if the extension is ambiguous.

3. **Error: Incorrect password for ZIP archive**:
    * Verify the password provided is correct.
    * Use a dictionary file with the `unlock` command to attempt password recovery.

4. **Error: No files specified to add to the archive**:
    * Provide a comma-separated list of files and directories to add using the `--files` option.
    * Ensure the paths are correct and the files/directories exist.

5. **Error: Extraction failed**:
    * Check if the archive is corrupted or password-protected.
    * Use the `repair` command to attempt to fix corrupted archives.

## Notes and Limitations

* Password dictionary required for unlock command
* Password recovery uses brute-force/dictionary attack
* Archive repair is experimental
* File paths in create/lock commands need comma separation
* Proper permissions required for operations

## License

[MIT License](license)
