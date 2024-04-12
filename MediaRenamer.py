import os
import re
import sys
import select
import datetime
import time
import signal
from PIL import Image
from PIL.ExifTags import TAGS
from collections import defaultdict


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# Messages
####################################################################################################
BANNER = """

░▒▓██████████████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓██████▓▒░                                   
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                                  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                                  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░                                  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                                  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                                  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                                  
                                                                                                    
                                                                                                    
░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 


"""
AUTHOR = "Author: Lu-Fu Chen\n"
VERSION = "Version: 1.0 (240412)\n"
INFO_ABORT = "\n[INFO] Process aborted. Have a nice day!"
INFO_CTRL_C = color.YELLOW + "[INFO] Press Ctrl+C to abort.\n" + color.END
INFO_RENAMED = "Renamed {filename} to {new_filename} [{renamed_count}/{total_count}]"
INFO_SKIPPED = (
    "Skipped {filename}: Already in correct format. [{renamed_count}/{total_count}]"
)
DIVIDER = "\n" + "_" * 72 + "\n"
RESULT_RENAMING_COMPLETE = "\n[INFO] Renaming process completed."
RESULT_REVERT_CHANGES = color.GREEN + "\n[RESULT] Changes reverted." + color.END
RESULT_CHANGES_SAVED = color.GREEN + "\n[RESULT] Changes saved." + color.END
ERROR_INVALID_INPUT = "[ERROR] Invalid input. Please enter 'Y' or 'N'."
ERROR_NO_MEDIA_FOUND = "[ERROR] No media found in the current directory."
INFO_FOUND_MEDIA = (
    color.YELLOW
    + ("[INFO] Found {photos_count} photos and {videos_count} videos in the directory.")
    + color.END
)
INFO_CHANGES_AUTO_SAVED = (
    color.YELLOW
    + ("[INFO] Changes will be saved automatically after a period of inactivity.")
    + color.END
)
INFO_SAVE_CHANGES = (
    color.BOLD + color.RED + "\nDo you want to save the changes? [Y/N]: " + color.END
)
INFO_RENAMING_IN_SECONDS = (
    color.GREEN + "\rRenaming the files in {remaining_time} seconds. " + color.END
)

RENAME_COUNTDOWN_DURATION = 10
REVERT_TIMEOUT_DURATION = 60

PHOTO_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".arw")
VIDEO_EXTENSIONS = (".mp4", ".mov", ".mkv")
####################################################################################################


def get_image_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date()
    except (FileNotFoundError, PermissionError, IOError):
        pass

    # If EXIF data is not available or failed to read, fall back to file creation date
    try:
        creation_time = os.stat(image_path).st_birthtime  # macOS-specific attribute
    except AttributeError:
        # For systems other than macOS
        creation_time = os.path.getctime(image_path)

    return datetime.date.fromtimestamp(creation_time)


def rename_photos(directory, photos_count, videos_count, media_extensions):
    serial_numbers = {}
    renamed_files = []
    renamed_count = 0
    total_count = photos_count + videos_count
    creation_times_by_date = (
        {}
    )  # Dictionary to store creation times of photos grouped by date
    file_by_creation_time = (
        {}
    )  # New dictionary to store file creation time and corresponding filenames
    existing_files = set(os.listdir(directory))

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        # Check if the file has one of the specified media extensions
        if filename.lower().endswith(media_extensions):
            image_path = os.path.join(directory, filename)
            date_taken = get_image_date(image_path)
            try:
                file_creation_time = os.stat(
                    image_path
                ).st_birthtime  # macOS-specific attribute
            except AttributeError:
                # For systems other than macOS
                file_creation_time = os.path.getctime(image_path)

            # Store creation times of photos grouped by date
            if date_taken not in creation_times_by_date:
                creation_times_by_date[date_taken] = []
            creation_times_by_date[date_taken].append(file_creation_time)
            file_by_creation_time[file_creation_time] = (
                filename  # Update the new dictionary
            )

    # Iterate over creation times of photos grouped by date
    for date_taken, creation_times in creation_times_by_date.items():
        # Sort creation times chronologically
        creation_times.sort()

        # Iterate over each photo taken on the same date
        for creation_time in creation_times:
            # Pull the corresponding filename from the new dictionary directly
            filename = file_by_creation_time[creation_time]
            image_path = os.path.join(directory, filename)
            base_filename, ext = os.path.splitext(filename)

            # Check if the base filename is already present, get the next available serial number
            serial_number = 1
            while (date_taken, serial_number) in serial_numbers:
                serial_number += 1

            # Construct the new filename with the appropriate serial number and extension
            new_filename = f"{date_taken}_{serial_number:03d}{ext.lower()}"
            new_path = os.path.join(directory, new_filename)

            # Update the serial number for the current date and serial number combination
            serial_numbers[(date_taken, serial_number)] = True

            # Rename the file
            if filename != new_filename:
                try:
                    os.rename(image_path, new_path)
                except (FileNotFoundError):
                    pass
                renamed_files.append((image_path, new_path))
                renamed_count += 1
                print(
                    INFO_RENAMED.format(
                        filename=filename,
                        new_filename=new_filename,
                        renamed_count=renamed_count,
                        total_count=total_count,
                    )
                )
            else:
                renamed_count += 1
                print(
                    INFO_SKIPPED.format(
                        filename=filename,
                        renamed_count=renamed_count,
                        total_count=total_count,
                    )
                )

    print(DIVIDER + RESULT_RENAMING_COMPLETE)
    return renamed_files


def revert_changes(renamed_files):
    for old_path, new_path in renamed_files:
        os.rename(new_path, old_path)
    print(RESULT_REVERT_CHANGES)


def countdown_timer(duration):
    start_time = time.time()
    print(INFO_CTRL_C)
    while True:
        time_elapsed = time.time() - start_time
        remaining_time = max(duration - int(time_elapsed), 0)
        if remaining_time == 0:
            print(
                "\r", end="", flush=True
            )  # Clear the line by printing a carriage return without any trailing characters
            break
        print(
            INFO_RENAMING_IN_SECONDS.format(remaining_time=remaining_time),
            end="",
            flush=True,
        )
        if time_elapsed >= duration:
            break
        time.sleep(1)


def signal_handler(sig, frame):
    print(INFO_ABORT)
    exit()


def input_with_timeout(prompt, timeout):
    print(prompt, end="", flush=True)
    i, _, _ = select.select([sys.stdin], [], [], timeout)
    if i:
        return input().strip().lower()
    else:
        print(RESULT_CHANGES_SAVED)
        exit()


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print(BANNER + AUTHOR + VERSION + DIVIDER)
    directory = os.getcwd()
    photos_count = 0
    videos_count = 0
    media_extensions = PHOTO_EXTENSIONS + VIDEO_EXTENSIONS

    for filename in os.listdir(directory):
        if filename.lower().endswith(PHOTO_EXTENSIONS):
            photos_count += 1
        elif filename.lower().endswith(VIDEO_EXTENSIONS):
            videos_count += 1
    if photos_count == 0 and videos_count == 0:
        print(ERROR_NO_MEDIA_FOUND)
        exit()
    else:
        print(
            INFO_FOUND_MEDIA.format(
                photos_count=photos_count, videos_count=videos_count
            )
        )

    countdown_timer(RENAME_COUNTDOWN_DURATION)
    user_input = None
    start_time = time.time()

    renamed_files = rename_photos(
        directory, photos_count, videos_count, media_extensions
    )
    print(INFO_CHANGES_AUTO_SAVED)
    while True:
        revert = input_with_timeout(INFO_SAVE_CHANGES, REVERT_TIMEOUT_DURATION)
        if revert == "n":
            revert_changes(renamed_files)
            break
        if revert == "y":
            print(RESULT_CHANGES_SAVED)
            exit()
        print(ERROR_INVALID_INPUT)
