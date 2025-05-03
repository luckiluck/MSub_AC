from utils import extract_season_episode
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
    pattern = r'(.*)(\s|-_|\[|第|_|\#|E)(\d{2,3})(\s|_|v\d{1}|\]|話|\..{3})(.*\.srt)'

    episode_numbers = []
    # Collect episode numbers from the filenames using extract_season_episode
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):
            season, episode = extract_season_episode(filename)
            if episode is not None:
                episode_numbers.append(episode)
            else:
                print(f"[\033[93mWarning\033[0m] No episode number found in {filename}")

    # Determine the start range, end range, and offset
    start_range = min(episode_numbers)
    end_range = max(episode_numbers)
    offset = 1 - start_range

    if start_range == 1:
        print(f"[\033[95mInfo\033[0m] Episode numbers already start from 01")
        return 2  # Return 2 if no renaming is needed

    # Rename files based on the calculated offset
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):  # Process only .srt files
            match = re.search(pattern, filename)
            if match:
                # Extract parts of the filename using regex groups
                prefix_1, prefix_2, episode_num, suffix_1, suffix_2 = match.groups()
                old_num = int(episode_num)
                if start_range <= old_num <= end_range:  # Check if episode number is in the range
                    new_num = old_num + offset  # Adjust the episode number
                    # Construct the new filename
                    new_filename = f"{prefix_1}{prefix_2}{new_num:02d}{suffix_1}{suffix_2}"
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_filename)
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f"[\033[95mInfo\033[0m] Renamed: {filename} -> {new_filename}")
            else:
                print(f"[\033[93mWarning\033[0m] No match found for {filename}")
                return 1  # Return 1 if no match is found

    print(f"[\033[92mInfo\033[0m] Episode numbers adjusted from {start_range} to {end_range} to start from 01 to {end_range + offset}.")

    return 0  # Return 0 if all files are processed successfully

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
#directory = 'D:\Python\MSub_AC\Japanese_Subtitles\K-ON! Live House!'  # Current directory, change this if needed
##add_season_number(directory,season_num=2)  # Change the season number as needed
#rename_subtitle_files(directory)

