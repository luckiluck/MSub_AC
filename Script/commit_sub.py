import os
import subprocess

def git_commit(folder_path, commit_message, push=False):
    try:
        # Change directory to the folder
        os.chdir(folder_path)

        # Check if there are .srt, .yaml, or .ass files in the current folder
        files_to_add = []
        for root, _, files in os.walk(folder_path):
            for f in files:
                if f.endswith((".srt", ".yaml", ".ass")):
                    files_to_add.append(os.path.join(root, f))
        if not files_to_add:
            print("[\033[91mError\033[0m] No .yaml, or .ass files to commit in the current folder.")
            exit(1)

        # Add only .srt, .yaml, and .ass files in the current folder to staging
        for file in files_to_add:
            subprocess.run(["git", "add", file], check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        print("[\033[92mInfo\033[0m] Changes committed successfully.")

        # Push the changes if push is True
        if push:
            subprocess.run(["git", "push"], check=True)
            print("[\033[92mInfo\033[0m] Changes pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[\033[91mError\033[0m] An error occurred: {e}")
    except FileNotFoundError:
        print("[\033[91mError\033[0m] Git is not installed or not found in PATH.")
    except Exception as e:
        print(f"[\033[91mError\033[0m] Unexpected error: {e}")