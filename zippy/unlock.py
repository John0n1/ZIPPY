import zipfile
import os

from .utils import handle_errors, loading_animation, validate_path, get_archive_type

PASSWORD_DICT_DEFAULT = "password_list.txt"

def unlock_archive(archive_path, dictionary_file=PASSWORD_DICT_DEFAULT, password=None, verbose=False, disable_animation=False):
    """
    Attempts to unlock a password-protected ZIP archive using a provided password or a dictionary attack.

    Parameters:
    - archive_path (str): Path to the archive file.
    - dictionary_file (str): Path to the dictionary file containing possible passwords.
    - password (str): Password for the archive (if known).
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If the archive type is unsupported or no passwords are provided.
    - RuntimeError: If unlocking fails due to incorrect password or other issues.
    """
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
