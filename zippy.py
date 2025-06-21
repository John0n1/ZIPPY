import os
import sys
import readline
import argparse
import logging
import json
from dotenv import load_dotenv
from zippy.extract import extract_archive
from zippy.create import create_archive
from zippy.list import list_archive_contents
from zippy.test import test_archive_integrity
from zippy.unlock import unlock_archive
from zippy.lock import lock_archive
from zippy.repair import repair_archive
from zippy.utils import (
    handle_errors, loading_animation, get_archive_type,
    validate_path, get_password_interactive, SUPPORTED_ARCHIVE_TYPES
)

load_dotenv()

SCRIPT_NAME = "ZIPPY"
VERSION = "0.3.0"
PASSWORD_DICT_DEFAULT = "password_list.txt"
CONFIG_FILE = "ZIPPY_config.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{SCRIPT_NAME} Version {VERSION}")

def display_help_text():
    print(f"\n{SCRIPT_NAME} - Archive Utility Toolkit (Version {VERSION})")
    print("-" * 50)
    print("Usage:")
    print(f"  {SCRIPT_NAME} <command> [archive_file] [options]")
    print("\nCommands:")
    print("  extract     Extract archive contents")
    print("  create      Create a new archive")
    print("  list        List contents of an archive")
    print("  test        Test archive integrity")
    print("  unlock      Attempt to unlock a password-protected archive")
    print("  lock        Create a password-protected archive (with file addition)")
    print("  repair      [Experimental] Attempt to repair a corrupted archive (Enhanced & Salvage!)")
    print("  help        Display this help message")
    print("  version     Show script version")
    print("\nOptions:")
    print("  -o, --output <path>     Specify output directory for extraction (default: current directory)")
    print("  -p, --password <password> Provide password for archive operations (lock, unlock, extract)")
    print("  -d, --dictionary <file>  Path to dictionary file for password cracking (unlock command)")
    print("  -f, --files <file1,file2,...> Files to add to a new archive (create, lock)")
    print("  --type <type>           Force archive type (zip, tar, tar.gz, gzip)")
    print("  --repair-mode <mode>    Repair mode for ZIP archives: 'remove_corrupted' (default), 'scan_only'")
    print("  --verbose               Enable verbose output")
    print("  --no-animation          Disable loading animation")
    print("  --save-config <file>    Save current settings to a configuration file")
    print("  --load-config <file>    Load settings from a configuration file")
    print("\nExamples:")
    print(f"  {SCRIPT_NAME} extract myarchive.zip")
    print(f"  {SCRIPT_NAME} extract myarchive.tar.gz -o extracted_files")
    print(f"  {SCRIPT_NAME} unlock protected.zip -d passwords.txt")
    print(f"  {SCRIPT_NAME} create new_archive.zip -f file1.txt,dir1,file2.jpg")
    print(f"  {SCRIPT_NAME} lock secure_archive.zip -p mySecretPassword")
    print(f"  {SCRIPT_NAME} lock locked_archive.zip -f documents,images -p SecurePass")
    print(f"  {SCRIPT_NAME} repair corrupted.zip --repair-mode remove_corrupted")
    print("\nSupported Archive Types:")
    print(", ".join(SUPPORTED_ARCHIVE_TYPES.keys()))
    print("\nNotes:")
    print("  - Password recovery (unlock) is a brute-force/dictionary attack and may take time.")
    print("  - Archive repair is experimental and may not work for all levels of corruption.")
    print("  - ZIP repair modes: 'scan_only' just checks, 'remove_corrupted' tries to fix by removing bad files.")
    print("  - For 'create' and 'lock' commands, list files/directories separated by commas (no spaces).")
    print("  - Ensure you have necessary permissions for file operations.")
    print("  - For severely corrupted archives, consider using dedicated repair tools.")
    print("  - Even if repair fails, salvage extraction will be attempted.")
    print("-" * 50)

def save_config(config, config_file=CONFIG_FILE):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    logging.info(f"Configuration saved to {config_file}")

def load_config(config_file=CONFIG_FILE):
    if not os.path.exists(config_file):
        handle_errors(f"Configuration file not found: {config_file}")
    with open(config_file, 'r') as f:
        config = json.load(f)
    logging.info(f"Configuration loaded from {config_file}")
    return config

def setup_auto_completion(commands):
    def completer(text, state):
        options = [cmd for cmd in commands if cmd.startswith(text)]
        return options[state] if state < len(options) else None
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

def main():
    display_banner()
    parser = argparse.ArgumentParser(description=f"{SCRIPT_NAME} - Archive Utility Toolkit (Version {VERSION})", add_help=False, usage=f"{SCRIPT_NAME} <command> [archive_file] [options]")
    parser.add_argument('command', choices=['extract', 'create', 'list', 'test', 'unlock', 'lock', 'repair', 'help', 'version'], help='Command to perform on the archive.')
    parser.add_argument('archive_file', nargs='?', help='Path to the archive file.')
    parser.add_argument('-o', '--output', dest='output_path', default='.', help='Output directory for extraction (default: current directory)')
    parser.add_argument('-p', '--password', dest='password', help='Password for archive operations')
    parser.add_argument('-d', '--dictionary', dest='dictionary_file', default=PASSWORD_DICT_DEFAULT, help='Path to dictionary file for password cracking (default: password_list.txt)')
    parser.add_argument('-f', '--files', dest='files_to_add', help='Comma-separated list of files/directories to add to the archive (create, lock)')
    parser.add_argument('--type', dest='archive_type', help='Force archive type (zip, tar, tar.gz, gzip)')
    parser.add_argument('--repair-mode', dest='repair_mode', default='remove_corrupted', choices=['remove_corrupted', 'scan_only'], help='Repair mode for ZIP archives (default: remove_corrupted)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output for debugging')
    parser.add_argument('--no-animation', action='store_true', help='Disable loading animation')
    parser.add_argument('--save-config', dest='save_config_file', help='Save current settings to a configuration file')
    parser.add_argument('--load-config', dest='load_config_file', help='Load settings from a configuration file')
    extract_group = parser.add_argument_group('extract command options')
    create_group = parser.add_argument_group('create command options')
    lock_group = parser.add_argument_group('lock command options')
    unlock_group = parser.add_argument_group('unlock command options')
    repair_group = parser.add_argument_group('repair command options')
    args = parser.parse_args()
    if args.save_config_file:
        config = vars(args)
        save_config(config, args.save_config_file)
        return
    if args.load_config_file:
        config = load_config(args.load_config_file)
        for key, value in config.items():
            if hasattr(args, key):
                setattr(args, key, value)
    if args.command == 'help':
        display_help_text()
    elif args.command == 'version':
        print(f"{SCRIPT_NAME} Version: {VERSION}")
    elif not args.archive_file and args.command not in ['help', 'version']:
        handle_errors("Archive file path is required for this command.")
    else:
        archive_path = args.archive_file
        if args.command in ['extract', 'list', 'test', 'unlock', 'repair']:
            validate_path(archive_path, "Archive file path", must_exist=True, is_dir=False)
        elif args.command in ['create', 'lock']:
            directory = os.path.dirname(os.path.abspath(archive_path)) or "."
            validate_path(directory, "Output directory", must_exist=True, is_dir=True)
        if args.command == 'extract':
            extract_archive(archive_path, args.output_path, args.password, args.verbose, args.no_animation)
        elif args.command == 'create':
            create_archive(archive_path, args.files_to_add, args.archive_type, args.password, args.verbose, args.no_animation)
        elif args.command == 'list':
            list_archive_contents(archive_path, args.verbose, args.no_animation)
        elif args.command == 'test':
            test_archive_integrity(archive_path, args.verbose, args.no_animation)
        elif args.command == 'unlock':
            unlock_archive(archive_path, args.dictionary_file, args.password, args.verbose, args.no_animation)
        elif args.command == 'lock':
            lock_archive(archive_path, args.files_to_add, "zip", args.password, args.verbose, args.no_animation)
        elif args.command == 'repair':
            repair_archive(archive_path, args.verbose, args.no_animation, args.repair_mode)
        else:
            print("Invalid command. See 'help'.")

if __name__ == "__main__":
    commands = ['extract', 'create', 'list', 'test', 'unlock', 'lock', 'repair', 'help', 'version']
    setup_auto_completion(commands)
    main()
