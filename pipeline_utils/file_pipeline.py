import os
import shutil


def archive_file(source_file_path):
    # Move file from landing to archive folder
    print("Archiving file...")
    target_directory = os.getenv("ARCHIVE_PATH")
    if target_directory:
        move_files(source_file_path, target_directory)
    else:
        print("ARCHIVE_PATH is not set.")


def quarantine_file(source_file_path):
    # Move file from landing to quarantine folder
    print("Quarantining file...")
    target_directory = os.getenv("QUARANTINE_PATH")
    if target_directory:
        move_files(source_file_path, target_directory)
    else:
        print("QUARANTINE_PATH is not set.")


def move_files(source_file_path, target_directory):
    try:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Build full target path (keeps the original filename)
        target_path = os.path.join(target_directory, os.path.basename(source_file_path))
        shutil.move(source_file_path, target_path)
        print(f"File moved to: {target_path}")
    except FileNotFoundError:
        print(f"Error: File '{source_file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied when moving '{source_file_path}'.")
    except Exception as e:
        print(f"Error moving file: {e}")
