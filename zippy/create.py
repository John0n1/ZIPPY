import zipfile
import tarfile
import gzip
import os
import shutil

from .utils import handle_errors, loading_animation, validate_path, get_archive_type

def _create_archive_internal(archive_path, files_to_add, archive_type, password, verbose, disable_animation):
    """
    Internal function to create an archive with the specified files.

    Parameters:
    - archive_path (str): Path to the output archive file.
    - files_to_add (str): Comma-separated list of files/directories to add to the archive.
    - archive_type (str): Type of the archive (zip, tar, tar.gz, gzip).
    - password (str): Password for encrypted archives (if applicable).
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If no files are specified to add to the archive.
    - RuntimeError: If archive creation fails due to various issues.
    """
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
    """
    Creates an archive with the specified files.

    Parameters:
    - archive_path (str): Path to the output archive file.
    - files_to_add (str): Comma-separated list of files/directories to add to the archive.
    - archive_type (str): Type of the archive (zip, tar, tar.gz, gzip).
    - password (str): Password for encrypted archives (if applicable).
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If no files are specified to add to the archive.
    - RuntimeError: If archive creation fails due to various issues.
    """
    if not files_to_add:
        files_to_add = input("Files to add not provided. Please enter the files to add (comma-separated): ")
    _create_archive_internal(archive_path, files_to_add, archive_type, password, verbose, disable_animation)
