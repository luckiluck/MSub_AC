import os
import subprocess
import sys

def git_commit(folder_path, commit_message, push=False):
    try:
        # Change directory to the folder
        os.chdir(folder_path)

        # Check if there are changes to commit
        #status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        #if not status_result.stdout.strip():
        #    print("\033[93mNo changes to commit. The folder is already up-to-date.\033[0m")
        #    return

        # Check if there are .srt or .yaml files to add
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        files_to_add = [line for line in status_result.stdout.splitlines() if line.endswith((".srt", ".yaml", ".ass"))]
        if not files_to_add:
            print("\033[91mNo .srt or .yaml files to commit.\033[0m")
            return

        # Add only .srt and .yaml files to staging
        subprocess.run(["git", "add", "*.srt", "*.yaml"], check=True)

        # Check if there are .ass files and add them if they exist
        ass_files = [f for f in os.listdir(folder_path) if f.endswith(".ass")]
        if ass_files:
            subprocess.run(["git", "add", "*.ass"], check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        print("\033[92mChanges committed successfully.\033[0m")

        # Push the changes if push is True
        if push:
            subprocess.run(["git", "push"], check=True)
            print("\033[92mChanges pushed successfully.\033[0m\n")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")
    except FileNotFoundError:
        print("\033[91mGit is not installed or not found in PATH.\033[0m")
    except Exception as e:
        print(f"\033[91mUnexpected error: {e}\033[0m")