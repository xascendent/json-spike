import os
import shutil

def reset_quarantine():
    # move files from quarantine to original folder
    print("Resetting quarantine...")
    original_directory = os.getenv("LANDING_PATH")
    source_directory = os.getenv("QUARANTINE_PATH")
    reset_files(source_directory, original_directory)

def reset_archive():
    # move files from archive to original folder
    print("Resetting archive...")
    original_directory = os.getenv("LANDING_PATH")
    source_directory = os.getenv("ARCHIVE_PATH")
    reset_files(source_directory, original_directory)        


def reset_files(source_directory, original_directory):    
    #loop through all files in quarantine folder
    #break apart file name using _ as delimiter and store the first item in a variable
    for file in os.listdir(source_directory):
        file_path = os.path.join(source_directory, file)
        parts = file.split('_')
        if len(parts) > 1:
            # move file to original folder
            destination = os.path.join(original_directory, parts[0])
            shutil.move(file_path, os.path.join(destination, file))
            print(f"Moved {file} to {destination}")