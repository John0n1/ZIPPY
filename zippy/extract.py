import zipfile
import tarfile
import gzip
import os
import shutil
import time
import sys

from .utils import handle_errors, loading_animation, get_archive_type

def extract_archive(archive_path, output_path=".", password=None, verbose=False, disable_animation=False):
    """
    Extracts the contents of an archive to the specified output directory.

    Parameters:
    - archive_path (str): Path to the archive file.
    - output_path (str): Directory where the contents will be extracted.
    - password (str): Password for encrypted archives (if applicable).
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If the archive type is unsupported.
    - RuntimeError: If extraction fails due to incorrect password or other issues.
    """
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
