import zipfile
import tarfile
import gzip
import os
import shutil

from .utils import handle_errors, loading_animation, get_archive_type, _salvage_extract_on_repair_fail, _tar_salvage_extraction

def repair_archive(archive_path, verbose=False, disable_animation=False, repair_mode="remove_corrupted"):
    """
    Repairs a corrupted archive.

    Parameters:
    - archive_path (str): Path to the archive file.
    - verbose (bool): Enable verbose output for debugging.
    - disable_animation (bool): Disable loading animation.
    - repair_mode (str): Repair mode for ZIP archives (default: remove_corrupted).

    Raises:
    - ValueError: If the archive type is unsupported.
    - RuntimeError: If repair fails due to various issues.
    """
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
