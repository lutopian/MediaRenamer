### Introduction

Media Renamer is a tool designed to help organize media files (photos and videos) within a directory by renaming them based on their creation dates. Here's a summary of what it does:

1. **Identification of Media Files**: It scans the current directory for media files such as photos (.jpg, .jpeg, .png, .webp, .arw) and videos (.mp4, .mov, .mkv) and counts the number of each type found.

2. **Extraction of Creation Dates**: For each media file, it attempts to extract the creation date. It first tries to retrieve the date from the EXIF metadata embedded in the media file. If the EXIF data is unavailable or cannot be read, it falls back to the file creation date.

3. **Renaming Process**: It renames each media file with a new filename format consisting of the creation date and a serial number. If multiple media files were created on the same date, they are numbered sequentially.

4. **User Interaction**:
    - Before proceeding with the renaming process, it initiates a countdown, allowing the user to abort the operation by pressing Ctrl+C.
    - After renaming, it prompts the user whether they want to save the changes or revert them.
    - If there's no response within a specified duration, it automatically saves the changes.

### Renaming Example

Let's say we have the following files with different creation dates:

1. `IMG_20220412.jpg` - Created on April 12, 2022 8AM
2. `DSC_20220412.jpg` - Created on April 12, 2022 9AM
3. `IMG_20220413.jpg` - Created on April 13, 2022 8AM
4. `VID_20220413.mp4` - Created on April 13, 2022 9AM

The renaming process would work as follows:

1. For `IMG_20220412.jpg` and `DSC_20220412.jpg` (both created on April 12, 2022):
   - The first file (`IMG_20220412.jpg`) would be renamed to `2022-04-12_001.jpg`.
   - The second file (`DSC_20220412.jpg`) would be renamed to `2022-04-12_002.jpg`.

2. For `IMG_20220413.jpg` (created on April 13, 2022):
   - The file would be renamed to `2022-04-13_001.jpg`.

3. For `VID_20220413.mp4` (created on April 13, 2022):
   - The file would be renamed to `2022-04-13_002.mp4`.

So, after the renaming process, the files would be named as follows:

1. `2022-04-12_001.jpg`
2. `2022-04-12_002.jpg`
3. `2022-04-13_001.jpg`
4. `2022-04-13_002.mp4`
