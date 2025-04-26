import zipfile
import os
import shutil

from .utils import handle_errors, loading_animation, validate_path, get_password_interactive, extract_archive, create_archive

def lock_archive(archive_path, files_to_add=None, archive_type="zip", password=None, verbose=False, disable_animation=False):
    """
    Creates a password-protected ZIP archive or re-locks an existing archive with a new password.

    Parameters:
    - archive_path (str): Path to the archive file.
    - files_to_add (str): Comma-separated list of files/directories to add to the archive.
    - archive_type (str): Type of the archive (default: "zip").
    - password (str): Password for the archive.
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If the archive type is unsupported or no files are specified.
    - RuntimeError: If locking fails due to incorrect password or other issues.
    """
    if archive_type != "zip":
        handle_errors("Locking (password protection) is only supported for ZIP archives.")
    if not password:
        password = get_password_interactive()
    if not files_to_add:
        files_to_add = input("Files to add not provided. Please enter the files to add (comma-separated): ")
    if files_to_add:
        create_archive(archive_path, files_to_add, archive_type, password, verbose, disable_animation)
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
