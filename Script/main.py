from auto_fill_msub import signin, fill_form, init_web_driver
from yaml_generator import generate_yaml
from commit_sub import git_commit
from rename_subtitle import rename_subtitle_files
from ass_to_srt import convert_ass_to_srt
from utils import load_config, get_git_status
import os
import json
import requests
import zipfile

def process_directory(directory, base_url, language, imdb):
    try:
        # Rename subtitle files if needed
        print(f"[\033[95mInfo\033[0m] Processing directory: {directory}")
        print("[\033[95mInfo\033[0m] Renaming subtitle files...")
        ret = rename_subtitle_files(directory)
        if ret == 1:
            print("[\033[91mError\033[0m] Failed to rename subtitle files.")
            return
        elif ret == 2:
            print("[\033[92mInfo\033[0m] No renaming needed.")
        else:
            print("[\033[92mInfo\033[0m] Subtitle files renamed successfully.")

        # Generate the YAML file for MSubtitles
        print("[\033[95mInfo\033[0m] Generating YAML file...")
        yaml_content = generate_yaml(directory, base_url)
        if yaml_content:
            print("[\033[92mInfo\033[0m] YAML file generated successfully.")
            movie = yaml_content[0]
            season = yaml_content[1]
            url = yaml_content[2]
            print("\033[94mAnime Title:\033[0m", yaml_content[0])
            print("\033[94mSeason:\033[0m", yaml_content[1])
            print("\033[94mYAML Link:\033[0m\n", yaml_content[2])
        else:
            print("\033[91mFailed to generate YAML file.\033[0m")
            return

        # Ask the user for confirmation before committing subtitles
        commit_message = f"Add \"{movie}\" subtitle(s)"
        print(f"\033[93mDo you want to commit&push the subtitles with the message: '{commit_message}'? (y/n)\033[0m")
        user_input = input().strip().lower()
        if user_input != 'y':
            print("[\033[93mWarning\033[0m] Subtitles were not committed.")
        else:
            git_commit(directory, commit_message, push=True)
            print("[\033[92mInfo\033[0m] Subtitles committed successfully.")

        # Check if URL is alive
        if url:
            response = requests.head(url)
            if response.status_code == 200:
                print("[\033[92mInfo\033[0m] YAML link is alive.")
            else:
                print("[\033[91mError\033[0m] YAML link is not alive.")
        else:
            print("\033[91mURL is empty.\033[0m")

        # Initialize the WebDriver
        chromedriver_path = 'D:\Program Files\chromedriver-win64\chromedriver.exe'
        driver = init_web_driver(chromedriver_path)

        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            credentials_path = os.path.join(script_dir, 'credentials')

            # Load credentials from the file
            with open(credentials_path, 'r') as file:
                credentials = json.load(file)

            username = credentials['username']
            password = credentials['password']

            # Sign in
            signin(driver, username, password)

            # Fill the form
            ret = fill_form(driver, movie, language, imdb, season, url)
            if ret == 1:
                # Retry the form submission
                max_retries = config.get("max_fill_form_retry", 3)
                for attempt in range(max_retries):
                    print(f"[\033[93mWarning\033[0m] Form submission failed. Retrying... (Attempt {attempt + 1}/{max_retries})")
                    ret = fill_form(driver, movie, language, imdb, season, url)
                    if ret != 1:
                        print("[\033[92mInfo\033[0m] Form submitted successfully after retry.")
                        break
                else:
                    print("[\033[91mError\033[0m] Failed to submit the form after maximum retries.")
        finally:
            # Close the browser
            #driver.quit()
            pass
    except Exception as e:
        print(f"[Error] An error occurred while processing {directory}: {e}")

if __name__ == "__main__":

    # Load configuration
    config = load_config()
    base_directories = config.get("base_directories", [])
    base_url = config.get("base_url", "")
    language = config.get("language", "Japanese")
    imdb = config.get("imdb", "kitsu")

    for base_directory in base_directories:
        try:
            # Get untracked or uncommitted folders using git
            folders = get_git_status(base_directory)
            for folder in folders:
                print("\n------------------------------")
                print(f"[\033[95mInfo\033[0m] Scanning folder: {folder}")

                # Check for .zip files and extract them
                for file in os.listdir(folder):
                    if file.endswith('.zip'):
                        zip_path = os.path.join(folder, file)
                        try:
                            print(f"[\033[95mInfo\033[0m] Extracting {zip_path}...")
                            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                zip_ref.extractall(folder)
                            os.remove(zip_path)
                            print(f"[\033[92mInfo\033[0m] Extracted and removed {zip_path}.")
                        except Exception as e:
                            print(f"[\033[91mError\033[0m] Failed to extract {zip_path}: {e}")

                # If the folder contains .ass files, create "ass" folder and move it there
                ass_files = [file for file in os.listdir(folder) if file.endswith('.ass')]
                if ass_files:
                    ass_folder = os.path.join(folder, "ass")
                    if not os.path.exists(ass_folder):
                        os.makedirs(ass_folder)

                    for file in ass_files:
                        source_path = os.path.join(folder, file)
                        destination_path = os.path.join(ass_folder, file)
                        os.rename(source_path, destination_path)
                        print(f"[\033[92mInfo\033[0m] Moved {file} to {ass_folder}.")
                        convert_ass_to_srt(ass_folder, folder)

                # Process the directory
                process_directory(folder, base_url, language, imdb)
        except Exception as e:
            print(f"[\033[91mError\033[0m] An error occurred while scanning {base_directory}: {e}")