from auto_fill_msub import signin, fill_form, init_web_driver
from yaml_generator import generate_yaml
from commit_sub import git_commit
import os
import json
import requests

# Main script
if __name__ == "__main__":
    # Set the subtitle directory and base Github URL
    base_directory = 'D:\Python\MSub_AC\Japanese_Subtitles\Denpa Kyoushi (TV)'  # USE OFFICIAL ANIME NAME FROM KITSU.IO. AVOID SYMBOLS IN FILENAME!!!
    base_url = 'https://raw.githubusercontent.com/luckiluck/MSub_AC/main/Japanese_Subtitles/'  # Replace with your actual base URL
    language = "Japanese"
    imdb = "kitsu"

    # Generate the YAML file for MSubtitles
    yaml_content = generate_yaml(base_directory, base_url)
    if yaml_content:
        print("\033[92mYAML file generated successfully.\033[0m")
        movie = yaml_content[0]
        season = yaml_content[1]
        url = yaml_content[2]
        print("\033[94mAnime Title:\033[0m", yaml_content[0])
        print("\033[94mSeason:\033[0m", yaml_content[1])
        print("\033[94mYAML Link:\033[0m\n", yaml_content[2])
    else:
        print("\033[91mFailed to generate YAML file.\033[0m")
        exit(1)

    # Ask the user for confirmation before committing subtitles
    commit_message = f"Add \"{movie}\" subtitle(s)"
    print(f"\033[93mDo you want to commit&push the subtitles with the message: '{commit_message}'? (y/n)\033[0m")
    user_input = input().strip().lower()
    if user_input != 'y':
        print("\033[92mSubtitles was not commited.\033[0m")
    else:
        git_commit(base_directory, commit_message, push=True)
        print("\033[92mSubtitles committed successfully.\033[0m")

        # Checl if url is alive
        if url:
            response = requests.head(url)
            if response.status_code == 200:
                print("\033[92mYAML link is alive.\033[0m")
            else:
                print("\033[91mYAML link is not alive.\033[0m")
                exit(1)
        else:
            print("\033[91mURL is empty.\033[0m")
            exit(1)

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
        fill_form(driver, movie, language, imdb, season, url)
    finally:
        # Close the browser
        #driver.quit()
        pass