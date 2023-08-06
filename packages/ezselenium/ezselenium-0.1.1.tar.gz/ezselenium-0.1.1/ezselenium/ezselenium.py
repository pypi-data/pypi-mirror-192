import argparse
import logging
import os
import platform
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--showwindow",
                    help="Show the browser window", action="store_true")
args = parser.parse_args()

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger("messageFollowers")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# If username was provided, use that as a postfix for the log file
log_file_name = "log.txt"

fh = logging.FileHandler(filename=log_file_name)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

SYSTEM = platform.system()

DRIVER = None

if SYSTEM == "Windows":
    from subprocess import CREATE_NO_WINDOW


def fail(msg):
    logger.error(msg)
    exit(1)


def get_chrome_version():
    stream = None

    if SYSTEM == "Windows":
        stream = os.popen(
            r"wmic datafile where name='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' get Version /value")
    elif SYSTEM == "Linux":
        stream = os.popen(r"google-chrome --version")
    else:
        fail("Could not determine chrome version for this platform")

    output = stream.read()

    chrome_version = None

    if SYSTEM == "Windows":
        chrome_version = re.sub(r".*?=", "", output).strip()
    elif SYSTEM == "Linux":
        chrome_version = re.sub(r"[^0-9.]", "", output).strip()

    if not chrome_version:
        fail("Could not find chrome version")

    logger.debug(f"Found chrome version {chrome_version}")

    return chrome_version.split(".")


def get_required_chromedriver(chrome_major_ver):
    chrome_major_ver = int(chrome_major_ver)

    valid_versions = []

    # Read all the chromedriver_"version".exe files and find all the valid versions
    for file in os.listdir(DIR_PATH + "/chromedrivers"):
        if file.startswith("chromedriver_"):
            version = None

            if SYSTEM == "Windows":
                version = file.split("_")[1].split(".")[0]
            elif SYSTEM == "Linux":
                version = file.split("_")[2]

            if version and version.isdigit():
                valid_versions.append(int(version))

    target_driver = ""

    if chrome_major_ver in valid_versions:
        if SYSTEM == "Windows":
            target_driver = DIR_PATH + \
                f"\\chromedrivers\\chromedriver_{chrome_major_ver}.exe"
        elif SYSTEM == "Linux":
            target_driver = DIR_PATH + \
                f"/chromedrivers/chromedriver_linux_{chrome_major_ver}"
    else:
        fail(f"Chrome version {chrome_major_ver} not supported")

    if not target_driver:
        fail("Could not determine the correct driver")

    return target_driver


def open_browser(driver_path="selenium.exe"):
    global DRIVER

    browserProfile = webdriver.ChromeOptions()
    browserProfile.add_argument("--disable-notifications")
    browserProfile.add_argument("--disable-extensions")
    browserProfile.add_experimental_option(
        'prefs', {'intl.accept_languages': 'en,en_US'})
    browserProfile.add_argument("--disable-infobars")
    browserProfile.add_argument("--disable-gpu")
    browserProfile.add_argument("--disable-dev-shm-usage")
    browserProfile.add_argument("--no-sandbox")
    if not args.showwindow:
        browserProfile.add_argument("--headless")

    # Create service object
    service = Service(driver_path)

    if SYSTEM == "Windows":
        service.creationflags = CREATE_NO_WINDOW

    logger.debug("Opening browser")

    DRIVER = webdriver.Chrome(service=service, options=browserProfile)

    # Put onto second monitor
    if args.showwindow:
        logger.debug("Moving browser to second screen on the right")
        DRIVER.set_window_position(2000, 0)
        DRIVER.maximize_window()

    return DRIVER

def load_browser():
    global DRIVER

    # Get chrome version
    logger.debug("Getting chrome version")
    chrome_version = get_chrome_version()
    logger.debug(f"Chrome version: {chrome_version}")

    # Get required chromedriver
    logger.debug("Getting required chromedriver")
    driver_path = get_required_chromedriver(chrome_version[0])
    logger.debug(f"Found chromedriver {driver_path}")

    # Open browser
    DRIVER = open_browser(driver_path)

    return DRIVER

if __name__ == "__main__":
    load_browser()

url = DRIVER.command_executor._url  # "http://127.0.0.1:60622/hub"
session_id = DRIVER.session_id