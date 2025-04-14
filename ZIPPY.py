import zipfile
import tarfile
import gzip
import os
import sys
import time
import argparse
import shutil
import getpass
import json
import readline
from dotenv import load_dotenv

load_dotenv()

SCRIPT_NAME = "ZIPPY"
VERSION = "0.3.0"
SUPPORTED_ARCHIVE_TYPES = {
    ".zip": "zip",
    ".tar": "tar",
    ".tar.gz": "tar.gz",
    ".tgz": "tar.gz",
    ".gz": "gzip"
}
LOADING_CHARS = ["/", "-", "\\", "|"]
PASSWORD_DICT_DEFAULT = "password_list.txt"
CONFIG_FILE = "ZIPPY_config.json"

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

def loading_animation(message="Processing...", duration=2, disable_animation=False):
    if disable_animation:
        print(f"{message} (Please wait...)")
        time.sleep(duration)
        return
    start_time = time.time()
    idx = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f"\r{message} {LOADING_CHARS[idx % len(LOADING_CHARS)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write(f"\r{message} Done!   \n")

def get_archive_type(archive_path, forced_type=None):
    if forced_type:
        if forced_type not in SUPPORTED_ARCHIVE_TYPES.values():
            raise ValueError(f"Invalid archive type specified: {forced_type}. Supported types: {', '.join(SUPPORTED_ARCHIVE_TYPES.values())}")
        return forced_type
    _, ext = os.path.splitext(archive_path)
    if ext.lower() in SUPPORTED_ARCHIVE_TYPES:
        return SUPPORTED_ARCHIVE_TYPES[ext.lower()]
    elif archive_path.lower().endswith(".tar.gz") or archive_path.lower().endswith(".tgz"):
        return "tar.gz"
    else:
        return None

def handle_errors(message, verbose=False, exit_code=1):
    print(f"Error: {message}")
    if verbose:
        import traceback
        traceback.print_exc()
    sys.exit(exit_code)

def validate_path(path, description="Path", must_exist=True, is_dir=False):
    if not path:
        handle_errors(f"{description} cannot be empty.")
    if must_exist and not os.path.exists(path):
        handle_errors(f"{description} not found: {path}")
    if is_dir and not os.path.isdir(path):
        handle_errors(f"{description} must be a directory: {path}")
    return os.path.abspath(path)

def get_password_interactive(prompt="Enter password: "):
    return getpass.getpass(prompt)

def save_config(config, config_file=CONFIG_FILE):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {config_file}")

def load_config(config_file=CONFIG_FILE):
    if not os.path.exists(config_file):
        handle_errors(f"Configuration file not found: {config_file}")
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"Configuration loaded from {config_file}")
    return config

def setup_auto_completion(commands):
    def completer(text, state):
        options = [cmd for cmd in commands if cmd.startswith(text)]
        return options[state] if state < len(options) else None
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

def extract_archive(archive_path, output_path=".", password=None, verbose=False, disable_animation=False):
    if not output_path:
        output_path = input("Output directory not provided. Please enter the output directory: ")
    archive_type = get_archive_type(archive_path)
    if not archive_type:
        handle_errors(f"Unsupported archive type for: {archive_path}")
    output_path = os.path.abspath(output_path)
    os.makedirs(output_path, exist_ok=True)
    try:
        loading_animation(f"Extracting {os.path.basename(archive_path)} to {output_path}", duration=2, disable_animation=disable_animation)
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                try:
                    zf.extractall(output_path, pwd=password.encode() if password else None)
                except RuntimeError as e:
                    if "password" in str(e).lower():
                        handle_errors("Incorrect password for ZIP archive.", verbose)
                    else:
                        handle_errors(f"ZIP Extraction error: {e}", verbose)
        elif archive_type in ["tar", "tar.gz"]:
            mode = 'r:gz' if archive_type == "tar.gz" else 'r'
            with tarfile.open(archive_path, mode) as tf:
                try:
                    tf.extractall(output_path)
                except tarfile.ReadError as e:
                    handle_errors(f"TAR Extraction error: {e}", verbose)
        elif archive_type == "gzip":
            output_file = os.path.join(output_path, os.path.splitext(os.path.basename(archive_path))[0])
            with gzip.open(archive_path, 'rb') as gf:
                with open(output_file, 'wb') as outfile:
                    shutil.copyfileobj(gf, outfile)
        else:
            handle_errors(f"Extraction for {archive_type} not implemented.", verbose)
        print(f"Successfully extracted to: {output_path}")
    except Exception as e:
        handle_errors(f"Extraction failed: {e}", verbose)

def _create_archive_internal(archive_path, files_to_add, archive_type, password, verbose, disable_animation):
    if not files_to_add:
        handle_errors("No files specified to add to the archive.")
    file_list = [f.strip() for f in files_to_add.split(',')]
    if not archive_type:
        archive_type = get_archive_type(archive_path)
        if not archive_type or archive_type == "gzip":
            handle_errors(f"Could not infer archive type from output path. Please specify with --type (zip, tar, tar.gz).")
    try:
        loading_animation(f"Creating {os.path.basename(archive_path)}", duration=2, disable_animation=disable_animation)
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                if password:
                    zf.setpassword(password.encode())
                for file_item in file_list:
                    file_item = validate_path(file_item, "File to add", must_exist=True, is_dir=False)
                    if os.path.isdir(file_item):
                        for root, _, files in os.walk(file_item):
                            for file in files:
                                filepath = os.path.join(root, file)
                                arcname = os.path.relpath(filepath, file_item)
                                zf.write(filepath, arcname=arcname)
                    else:
                        zf.write(file_item, arcname=os.path.basename(file_item))
        elif archive_type == "tar":
            with tarfile.open(archive_path, 'w') as tf:
                for file_item in file_list:
                    file_item = validate_path(file_item, "File to add", must_exist=True, is_dir=False)
                    tf.add(file_item)
        elif archive_type == "tar.gz":
            with tarfile.open(archive_path, 'w:gz') as tf:
                for file_item in file_list:
                    file_item = validate_path(file_item, "File to add", must_exist=True, is_dir=False)
                    tf.add(file_item)
        elif archive_type == "gzip":
            if len(file_list) != 1:
                handle_errors("gzip archives can only contain a single file. Please specify one file to compress.")
            input_file = validate_path(file_list[0], "File to gzip", must_exist=True, is_dir=False)
            with open(input_file, 'rb') as infile, gzip.open(archive_path, 'wb') as gf:
                shutil.copyfileobj(infile, gf)
        else:
            handle_errors(f"Creation for {archive_type} not implemented.", verbose)
        print(f"Successfully created archive: {archive_path}")
    except Exception as e:
        handle_errors(f"Archive creation failed: {e}", verbose)

def create_archive(archive_path, files_to_add, archive_type=None, password=None, verbose=False, disable_animation=False):
    if not files_to_add:
        files_to_add = input("Files to add not provided. Please enter the files to add (comma-separated): ")
    _create_archive_internal(archive_path, files_to_add, archive_type, password, verbose, disable_animation)

def lock_archive(archive_path, files_to_add=None, archive_type="zip", password=None, verbose=False, disable_animation=False):
    if archive_type != "zip":
        handle_errors("Locking (password protection) is only supported for ZIP archives.")
    if not password:
        password = get_password_interactive()
    if not files_to_add:
        files_to_add = input("Files to add not provided. Please enter the files to add (comma-separated): ")
    if files_to_add:
        _create_archive_internal(archive_path, files_to_add, archive_type, password, verbose, disable_animation)
    else:
        if not os.path.exists(archive_path):
            handle_errors(f"Archive file not found: {archive_path}. Cannot lock a non-existent archive.")
        temp_dir = "zippsnipp_temp_relock"
        os.makedirs(temp_dir, exist_ok=True)
        try:
            loading_animation(f"Re-locking {os.path.basename(archive_path)} with password", duration=2, disable_animation=disable_animation)
            extract_archive(archive_path, temp_dir, verbose=verbose, disable_animation=True)
            files = ",".join([os.path.join(temp_dir, f) for f in os.listdir(temp_dir)])
            create_archive(archive_path, files, "zip", password, verbose, disable_animation=True)
            shutil.rmtree(temp_dir)
            print(f"Successfully re-locked archive: {archive_path} (Password protected)")
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            handle_errors(f"Failed to re-lock archive: {e}", verbose)

def list_archive_contents(archive_path, verbose=False, disable_animation=False):
    archive_type = get_archive_type(archive_path)
    if not archive_type:
        handle_errors(f"Unsupported archive type for: {archive_path}")
    try:
        loading_animation(f"Listing contents of {os.path.basename(archive_path)}", duration=1, disable_animation=disable_animation)
        print(f"\nContents of {archive_path}:\n")
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                for name in zf.namelist():
                    print(name)
        elif archive_type in ["tar", "tar.gz"]:
            with tarfile.open(archive_path, 'r:*') as tf:
                for member in tf.getnames():
                    print(member)
        elif archive_type == "gzip":
            print("This is a gzip file. Use 'extract' command to see the content after decompression.")
        else:
            handle_errors(f"Listing contents for {archive_type} not implemented.", verbose)
    except Exception as e:
        handle_errors(f"Failed to list archive contents: {e}", verbose)

def test_archive_integrity(archive_path, verbose=False, disable_animation=False):
    archive_type = get_archive_type(archive_path)
    if not archive_type:
        handle_errors(f"Unsupported archive type for: {archive_path}")
    try:
        loading_animation(f"Testing integrity of {os.path.basename(archive_path)}", duration=1, disable_animation=disable_animation)
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                result = zf.testzip()
                if result is None:
                    print(f"Integrity test for {archive_path}: [OK]")
                else:
                    handle_errors(f"Integrity test failed for {archive_path}. Corrupted file: {result}", exit_code=2)
        elif archive_type in ["tar", "tar.gz"]:
            try:
                with tarfile.open(archive_path, 'r:*') as tf:
                    tf.getnames()
                print(f"Integrity test for {archive_path}: [OK] (Basic check)")
            except tarfile.ReadError as e:
                handle_errors(f"Integrity test failed for {archive_path}. Possible corruption: {e}", exit_code=2)
        elif archive_type == "gzip":
            try:
                with gzip.open(archive_path, 'rb') as gf:
                    gf.read(1024)
                print(f"Integrity test for {archive_path}: [OK] (Basic gzip check)")
            except gzip.BadGzipFile as e:
                handle_errors(f"Integrity test failed for {archive_path}. Possible corruption: {e}", exit_code=2)
        else:
            handle_errors(f"Integrity test for {archive_type} not implemented.", verbose)
    except Exception as e:
        handle_errors(f"Integrity test could not be performed: {e}", verbose)

def unlock_archive(archive_path, dictionary_file=PASSWORD_DICT_DEFAULT, password=None, verbose=False, disable_animation=False):
    archive_type = get_archive_type(archive_path)
    if archive_type != "zip":
        handle_errors("Unlock operation is only supported for ZIP archives at this time.")
    if not password and not dictionary_file:
        handle_errors("Please provide a password or a dictionary file for unlocking.")
    if dictionary_file:
        dictionary_path = validate_path(dictionary_file, "Dictionary file", must_exist=True, is_dir=False)
    if password:
        passwords_to_try = [password]
    elif dictionary_file:
        try:
            with open(dictionary_path, 'r', encoding='latin-1') as df:
                passwords_to_try = [line.strip() for line in df]
        except FileNotFoundError:
            handle_errors(f"Dictionary file not found: {dictionary_path}")
        except Exception as e:
            handle_errors(f"Error reading dictionary file: {e}", verbose)
    else:
        handle_errors("No passwords to try for unlocking.")
    try:
        loading_animation(f"Attempting to unlock {os.path.basename(archive_path)}", duration=2, disable_animation=disable_animation)
        found_password = False
        for pwd in passwords_to_try:
            try_password = pwd.encode('utf-8', errors='ignore')
            try:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    zf.extractall(pwd=try_password)
                print(f"\nPassword found: {pwd}")
                found_password = True
                break
            except RuntimeError as e:
                if "bad password" in str(e).lower() or "incorrect password" in str(e).lower():
                    if verbose:
                        print(f"Trying password: {pwd} - Failed")
                    continue
                else:
                    handle_errors(f"Unlock attempt failed due to: {e}", verbose)
                    break
            except Exception as e:
                handle_errors(f"Unlock attempt failed unexpectedly: {e}", verbose)
                break
        if not found_password:
            print("\nPassword not found in the provided list.")
            if dictionary_file:
                print(f"Tried passwords from dictionary: {dictionary_file}")
            if password:
                print(f"Tried password: {password}")
    except Exception as e:
        handle_errors(f"Password unlocking process failed: {e}", verbose)

def _salvage_extract_on_repair_fail(archive_path, output_dir_name, archive_type, verbose):
    salvage_output_path = os.path.join(os.getcwd(), output_dir_name)
    os.makedirs(salvage_output_path, exist_ok=True)
    extracted_count = 0
    print(f"\n[Salvage Extraction Attempt] Repair failed. Attempting to extract salvageable content to: {salvage_output_path}")
    try:
        if archive_type == "zip":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                for member in zf.infolist():
                    try:
                        zf.extract(member, path=salvage_output_path)
                        extracted_count += 1
                        if verbose:
                            print(f"  Salvaged: {member.filename}")
                    except Exception as e_extract:
                        print(f"Warning: Could not salvage {member.filename}. Error: {e_extract}")
        elif archive_type in ["tar", "tar.gz"]:
            extracted_count = _tar_salvage_extraction(archive_path, salvage_output_path, verbose)
        elif archive_type == "gzip":
            output_file_name = os.path.join(salvage_output_path, os.path.splitext(os.path.basename(archive_path))[0] + "_salvaged")
            try:
                with gzip.open(archive_path, 'rb') as gf:
                    with open(output_file_name, 'wb') as outfile:
                        shutil.copyfileobj(gf, outfile)
                extracted_count = 1
                print(f"  Salvaged (decompressed) content to: {output_file_name}")
            except Exception as e_gzip_salvage:
                print(f"Warning: GZIP salvage decompression failed. Error: {e_gzip_salvage}")
        else:
            print(f"Salvage extraction not implemented for {archive_type} yet.")
        if extracted_count > 0:
            print(f"Salvage extraction completed. {extracted_count} files/items extracted to: {salvage_output_path}")
        else:
            print("No files could be salvaged from the archive.")
    except Exception as e_salvage_overall:
        print(f"Error during salvage extraction process: {e_salvage_overall}")
        print("Extraction may be incomplete.")

def _tar_salvage_extraction(archive_path, output_dir, verbose):
    extracted_count = 0
    try:
        with tarfile.open(archive_path, 'r:*') as tf:
            for member in tf.getmembers():
                try:
                    tf.extract(member, path=output_dir)
                    extracted_count += 1
                    if verbose:
                        print(f"  Extracted: {member.name}")
                except tarfile.ReadError as e_extract:
                    print(f"Warning: Could not extract {member.name}. Error: {e_extract}")
                except Exception as e_extract_other:
                    print(f"Warning: Extraction error for {member.name}. Error: {e_extract_other}")
    except Exception as e_tar_open:
        print(f"Warning: Could not open TAR archive for salvage extraction. Error: {e_tar_open}")
    return extracted_count

def repair_archive(archive_path, verbose=False, disable_animation=False, repair_mode="remove_corrupted"):
    archive_type = get_archive_type(archive_path)
    if archive_type not in ["zip", "tar", "gzip"] and archive_type != "tar.gz":
        handle_errors("Repair operation is only supported for ZIP, TAR, and GZIP archives at this time.")
    print("[Experimental Feature] Archive repair is a complex process and may not always be successful.")
    print(f"Repair mode: {repair_mode}")
    repair_attempted = False
    try:
        loading_animation(f"Attempting to repair {os.path.basename(archive_path)}", duration=3, disable_animation=disable_animation)
        if archive_type == "zip":
            try:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    bad_file = zf.testzip()
                    if bad_file:
                        print(f"Possible corruption detected in: {bad_file}")
                        if repair_mode == "remove_corrupted":
                            repair_attempted = True
                            print(f"Attempting to repair by removing corrupted file: {bad_file}...")
                            temp_zip_path = archive_path + ".temp_repair.zip"
                            with zipfile.ZipFile(temp_zip_path, 'w') as temp_zf:
                                with zipfile.ZipFile(archive_path, 'r') as original_zf:
                                    for item in original_zf.infolist():
                                        if item.filename != bad_file:
                                            try:
                                                data = original_zf.read(item.filename)
                                                temp_zf.writestr(item, data)
                                            except Exception as e_read:
                                                print(f"Warning: Could not copy {item.filename}. Error: {e_read}")
                            os.remove(archive_path)
                            os.rename(temp_zip_path, archive_path)
                            print(f"Repair finished. Corrupted file '{bad_file}' removed. Repaired archive: {archive_path}")
                        elif repair_mode == "scan_only":
                            print("Scan-only mode: Reporting corrupted file but not attempting repair.")
                        else:
                            print(f"Unknown repair mode: {repair_mode}. No repair action taken.")
                    else:
                        print(f"Integrity check passed for {archive_path}. No major errors detected.")
            except zipfile.BadZipFile as e:
                print(f"ZIP archive appears to be badly corrupted: {e}")
                print("Specialized ZIP repair tools may be required.")
            except Exception as e:
                handle_errors(f"Error during ZIP repair attempt: {e}", verbose)
        elif archive_type in ["tar", "tar.gz"]:
            repair_attempted = True
            print("Enhanced TAR repair: Attempting to extract readable files...")
            extracted_files_dir = f"{os.path.basename(archive_path)}_extracted_during_repair"
            os.makedirs(extracted_files_dir, exist_ok=True)
            extracted_count = _tar_salvage_extraction(archive_path, extracted_files_dir, verbose)
            if extracted_count > 0:
                print(f"Extracted {extracted_count} files from TAR archive to: {extracted_files_dir}")
                print("This is a salvage operation. The original archive may still be corrupted.")
            else:
                print("No files could be extracted from the TAR archive. It may be severely corrupted.")
        elif archive_type == "gzip":
            repair_attempted = True
            print("GZIP repair: Attempting basic decompression to salvage content...")
            output_file_name = f"{os.path.splitext(os.path.basename(archive_path))[0]}_recovered"
            try:
                with gzip.open(archive_path, 'rb') as gf:
                    with open(output_file_name, 'wb') as outfile:
                        shutil.copyfileobj(gf, outfile)
                print(f"Successfully decompressed content from gzip archive to: {output_file_name}")
            except gzip.BadGzipFile as e:
                print(f"GZIP archive appears to be corrupted: {e}")
                print("Specialized GZIP repair tools may be required.")
            except Exception as e:
                handle_errors(f"Error during GZIP repair attempt: {e}", verbose)
        print("[Repair attempt finished. Results may vary.]")
        if not repair_attempted and archive_type != "gzip":
            print("No repair action taken based on the integrity check (or in scan_only mode).")
        if repair_attempted or archive_type == "gzip":
            salvage_output_dir_name = f"{os.path.basename(archive_path)}_salvaged_content"
            _salvage_extract_on_repair_fail(archive_path, salvage_output_dir_name, archive_type, verbose)
        print("It's recommended to have backups of important archives.")
    except Exception as e:
        handle_errors(f"Repair operation failed: {e}", verbose)

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

