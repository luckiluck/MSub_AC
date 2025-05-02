from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select  # Import Select class

def signin(driver, username, password):
    try:
        # Open the login page
        driver.get("https://msubtitles.lowlevel1989.click/accounts/login/")

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)

        # Fill in the Username field
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.clear()
        username_field.send_keys(username)

        # Fill in the Password field
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        print("\033[92mSigned in successfully!\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred during sign-in: {e}\033[0m")

def fill_form(driver, movie, language, imdb, season, url):
    try:
        # Open the target URL
        driver.get("https://msubtitles.lowlevel1989.click/dashboard/subtitle/")

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)

        # Fill in the Movie field
        movie_field = wait.until(EC.presence_of_element_located((By.ID, "id_movie")))
        movie_field.clear()
        movie_field.send_keys(movie)

        # Select the Language field
        language_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "id_lang"))))
        language_dropdown.select_by_visible_text(language)

        # Fill in the Imdb field
        imdb_field = driver.find_element(By.NAME, "imdb")
        imdb_field.clear()
        imdb_field.send_keys(imdb)

        # Fill in the Season field
        season_field = driver.find_element(By.ID, "id_season")
        season_field.clear()
        season_field.send_keys(int(season))  # Ensure the value is entered as a number

        # Fill in the Url field
        url_field = driver.find_element(By.NAME, "url")
        url_field.clear()
        url_field.send_keys(url)

        # Submit the form (if there's a submit button)
        #submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        #submit_button.click()

        print("\033[92mForm submitted successfully!\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred while filling the form: {e}\033[0m")

def init_web_driver(chromedriver_path):
    """
    Initializes and returns a Chrome WebDriver instance.

    Args:
        chromedriver_path (str): The path to the ChromeDriver executable.

    Returns:
        WebDriver: An instance of the Chrome WebDriver.
    """
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

