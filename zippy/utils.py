import os
import sys
import time
import getpass
import json
import logging

# Constants from main zippy.py
SUPPORTED_ARCHIVE_TYPES = {
    ".zip": "zip",
    ".tar": "tar",
    ".tar.gz": "tar.gz",
    ".tgz": "tar.gz",
    ".gz": "gzip"
}
LOADING_CHARS = ["/", "-", "\\", "|"]

def loading_animation(message="Processing...", duration=2, disable_animation=False):
    """Display a loading animation while processing."""
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
    """Determine the archive type from file extension or forced type."""
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
    """Handle errors with logging and optional verbose output."""
    logging.error(message)
    if verbose:
        import traceback
        traceback.print_exc()
    sys.exit(exit_code)

def validate_path(path, description="Path", must_exist=True, is_dir=False):
    """Validate and return absolute path."""
    if not path:
        handle_errors(f"{description} cannot be empty.")
    if must_exist and not os.path.exists(path):
        handle_errors(f"{description} not found: {path}")
    if is_dir and not os.path.isdir(path):
        handle_errors(f"{description} must be a directory: {path}")
    return os.path.abspath(path)

def get_password_interactive(prompt="Enter password: "):
    """Get password input interactively."""
    return getpass.getpass(prompt)

# Salvage functions referenced in repair.py but missing
def _salvage_extract_on_repair_fail(archive_path, output_path=".", archive_type=None, verbose=False):
    """Attempt salvage extraction when repair fails."""
    try:
        logging.info(f"Attempting salvage extraction for {archive_path}...")
        # Import here to avoid circular imports
        from .extract import extract_archive
        extract_archive(archive_path, output_path, verbose=verbose, disable_animation=True)
        logging.info("Salvage extraction completed successfully.")
        return True
    except Exception as e:
        if verbose:
            logging.info(f"Salvage extraction failed: {e}")
        return False

def _tar_salvage_extraction(archive_path, output_path=".", verbose=False):
    """Attempt salvage extraction for TAR archives."""
    import tarfile
    extracted_count = 0
    try:
        print(f"Attempting TAR salvage extraction for {archive_path}...")
        with tarfile.open(archive_path, 'r:*', ignore_zeros=True) as tf:
            # Try to extract what we can
            for member in tf:
                try:
                    tf.extract(member, output_path)
                    extracted_count += 1
                except Exception as e:
                    if verbose:
                        print(f"Failed to extract {member.name}: {e}")
                    continue
        print(f"TAR salvage extraction completed. Extracted {extracted_count} files.")
        return extracted_count
    except Exception as e:
        if verbose:
            print(f"TAR salvage extraction failed: {e}")
        return 0

# Functions imported by lock.py - use lazy imports to avoid circular dependencies
def extract_archive(*args, **kwargs):
    """Wrapper for extract_archive to avoid circular imports."""
    from .extract import extract_archive as _extract_archive
    return _extract_archive(*args, **kwargs)

def create_archive(*args, **kwargs):
    """Wrapper for create_archive to avoid circular imports."""
    from .create import create_archive as _create_archive
    return _create_archive(*args, **kwargs)