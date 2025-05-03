import os
import re
import json
import subprocess
from urllib.parse import quote

def extract_season_episode(filename):
    match = re.search(r'S(\d+)E(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))

    season = None
    match = re.search(r'\sS(\d+)', filename)
    if match:
        season = int(match.group(1))

    episode = None
    match = re.search(r'E(\d+)', filename)
    if match:
        episode = int(match.group(1))

    match = re.search(r'(?:\s|-_|\[|第|_|\#)(\d{2,3})(?:\s|_|v\d{1}|\]|話|\..{3})', filename)
    if match:
        return season if season is not None else 1, int(match.group(1))

    if episode is None:
        print("[\033[93mWarning\033[0m] No episode number found in", filename)
        episode = 1

    if season is None:
        season = 1

    return season, episode

def url_encode_path(path):
    # Convert backslashes to forward slashes and encode
    path = path.replace('\\', '/')
    return quote(path)

# Load configuration from config.json
def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"[\033[91mError\033[0m] Failed to load configuration: {e}")
        return {}

def get_git_status(base_directory):
    try:
        # Run git status to find untracked and uncommitted folders
        result = subprocess.run(
            ["git", "-C", base_directory, "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        folders = set()
        for line in lines:
            if line.startswith("??") or line.startswith(" M"):
                # Extract only the folder name relative to base_directory
                relative_path = line[3:].strip().strip('"')
                full_path = os.path.normpath(os.path.join(base_directory, relative_path)).replace("\\Japanese_Subtitles\\Japanese_Subtitles", "\\Japanese_Subtitles").replace("\\Japanese_Drama\\Japanese_Drama", "\\Japanese_Drama")
                if os.path.exists(full_path) and os.path.isdir(full_path):
                    folders.add(full_path)
        return list(folders)
    except subprocess.CalledProcessError as e:
        print(f"[\033[91mError\033[0m] Failed to get git status: {e}")
        return []