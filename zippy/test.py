import zipfile
import tarfile
import gzip

from .utils import handle_errors, loading_animation, get_archive_type

def test_archive_integrity(archive_path, verbose=False, disable_animation=False):
    """
    Tests the integrity of an archive.

    Parameters:
    - archive_path (str): Path to the archive file.
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.

    Raises:
    - ValueError: If the archive type is unsupported.
    - RuntimeError: If integrity test fails due to various issues.
    """
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
