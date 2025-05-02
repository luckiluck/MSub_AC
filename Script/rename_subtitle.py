import os
import re

def rename_subtitle_files(directory):
    """
    Renames subtitle files in the specified directory by adjusting episode numbers
    so that the episodes always start with episode 01.

    Args:
        directory (str): The path to the directory containing the subtitle files.
    """
    # Regular expression to match the file pattern
    pattern = r'(.*S\d{2}E)(\d{2})(.*\.srt)'

    # Collect all episode numbers to determine the range
    episode_numbers = []
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):  # Process only .srt files
            match = re.match(pattern, filename)
            if match:
                episode_num = int(match.group(2))
                episode_numbers.append(episode_num)

    if not episode_numbers:
        print("No valid subtitle files found.")
        return

    # Determine the start range, end range, and offset
    start_range = min(episode_numbers)
    end_range = max(episode_numbers)
    offset = 1 - start_range

    # Rename files based on the calculated offset
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):  # Process only .srt files
            match = re.match(pattern, filename)
            if match:
                # Extract parts of the filename using regex groups
                prefix, episode_num, suffix = match.groups()
                old_num = int(episode_num)
                if start_range <= old_num <= end_range:  # Check if episode number is in the range
                    new_num = old_num + offset  # Adjust the episode number
                    # Construct the new filename
                    new_filename = f"{prefix}{new_num:02d}{suffix}"
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_filename)
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_filename}")

def add_season_number(directory,season_num=1):
    """
    Adds the season number to the subtitle files in the specified directory.

    Args:
        directory (str): The path to the directory containing the subtitle files.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):
            # Add season number while preserving the original episode number
            new_filename = re.sub(r'- (\d{2})', fr'- S{season_num:02d}E\1', filename)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

# Usage
directory = 'D:\Python\MSub_AC\Japanese_Subtitles\Aldnoah.Zero 2'  # Current directory, change this if needed
#add_season_number(directory,season_num=2)  # Change the season number as needed
rename_subtitle_files(directory)

