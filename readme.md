# John0n1/ZIPPY

ZIPPY is a robust, production-ready command-line archive utility toolkit that provides extraction, archive creation, listing, integrity testing, password unlocking, and experimental archive repair functionalities. It supports multiple archive formats such as ZIP, TAR, TAR.GZ, and GZIP.

## Features

- Extract archives in various formats.
- Create new archives and add multiple files/directories.
- List contents of an archive.
- Test archive integrity.
- Unlock password-protected ZIP archives using a provided password or a dictionary attack.
- Create password-protected (locked) ZIP archives.
- Experimental archive repair with salvage extraction for corrupted archives.
- Animated loading indicator with an option to disable it.
- Save and load configuration settings via JSON files.
- Command-line auto-completion using Python’s readline module.

## Requirements

- Python 3.12+
- [python-dotenv](https://pypi.org/project/python-dotenv/)

# Install dependencies using:

```bash
pip install python-dotenv
```
## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/John0n1/ZIPPY.git
cd ZIPPY
```

## Usage

ZIPPY is operated through the command line. Below are some examples:

### Extract an Archive
```python
python zippy.py extract myarchive.zip -o extracted_files
```
### Create a New Archive
```python
python zippy.py create new_archive.zip -f file1.txt,dir1,file2.jpg
```
### List Archive Contents
```python
python zippy.py list myarchive.tar.gz
```
### Test Archive Integrity
```python
python zippy.py test myarchive.zip
```
### Unlock a Password-Protected Archive
```python
python zippy.py unlock protected.zip -d passwords.txt
```
### Create a Password-Protected Archive
```python
python zippy.py lock secure_archive.zip -f documents,images -p SecurePass
```
### Repair a Corrupted Archive (Experimental)
```python
python zippy.py repair corrupted.zip --repair-mode remove_corrupted
```
### Show Help
```python
python zippy.py help
```
### Display Version
```python
python zippy.py version
```
## Configuration

You can save and load configuration settings using JSON files.

### Save Configuration:
```python
python zippy.py <command> <archive_file> [options] --save-config your_config.json
```
### Load Configuration:
```python
python zippy.py <command> <archive_file> [options] --load-config your_config.json
```

# Supported Archive Formats

ZIP

TAR

TAR.GZ / TGZ

GZIP (single file only)


# Auto-Completion

ZIPPY sets up basic auto-completion for commands using Python’s readline module. This feature is automatically enabled when running the script.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with any improvements or bug fixes.

## Disclaimer

ZIPPY is provided "as is" without warranty of any kind. Use at your own risk. Always keep backups of important archives.



