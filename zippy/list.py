import zipfile
import tarfile
import gzip
import os

from .utils import handle_errors, loading_animation, get_archive_type

def list_archive_contents(archive_path, verbose=False, disable_animation=False):
    """
    Lists the contents of an archive.

    Parameters:
    - archive_path (str): Path to the archive file.
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If the archive type is unsupported.
    - RuntimeError: If listing fails due to various issues.
    """
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
