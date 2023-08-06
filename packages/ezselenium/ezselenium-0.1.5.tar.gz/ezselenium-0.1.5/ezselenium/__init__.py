import argparse
import logging
import os
import platform
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

LOGGER = None

SYSTEM = platform.system()

DRIVER = None

if SYSTEM == "Windows":
    from subprocess import CREATE_NO_WINDOW


def fail(msg):
    LOGGER.error(msg)
    exit(1)


def log(msg):
    if LOGGER:
        LOGGER.debug(msg)


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

    log(f"Found chrome version {chrome_version}")

    return chrome_version.split(".")


def get_required_chromedriver(chrome_major_ver, driver_dir=None):
    if not driver_dir:
        driver_dir = DIR_PATH + "/chromedrivers"

    chrome_major_ver = int(chrome_major_ver)

    valid_versions = []

    # Read all the chromedriver_"version".exe files and find all the valid versions
    for file in os.listdir(driver_dir):
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
            target_driver = driver_dir + \
                f"\\chromedriver_{chrome_major_ver}.exe"
        elif SYSTEM == "Linux":
            target_driver = driver_dir + \
                f"/chromedriver_linux_{chrome_major_ver}"
    else:
        fail(f"Chrome version {chrome_major_ver} not supported")

    if not target_driver:
        fail("Could not determine the correct driver")

    return target_driver


def open_browser(driver_path="selenium.exe", headless=True):
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
    if headless:
        browserProfile.add_argument("--headless")

    # Create service object
    service = Service(driver_path)

    if SYSTEM == "Windows":
        service.creationflags = CREATE_NO_WINDOW

    log("Opening browser")

    DRIVER = webdriver.Chrome(service=service, options=browserProfile)

    # Put onto second monitor
    if not headless:
        log("Moving browser to second screen on the right")
        DRIVER.set_window_position(2000, 0)
        DRIVER.maximize_window()

    return DRIVER


def load_browser(driver_dir=None, headless=True):
    global DRIVER

    # Get chrome version
    log("Getting chrome version")
    chrome_version = get_chrome_version()
    log(f"Chrome version: {chrome_version}")

    # Get required chromedriver
    log("Getting required chromedriver")

    driver_path = get_required_chromedriver(
        chrome_version[0], driver_dir=driver_dir)

    log(f"Found chromedriver {driver_path}")

    # Open browser
    DRIVER = open_browser(driver_path, headless=headless)

    return DRIVER


if __name__ == "__main__":
    LOGGER = logging.getLogger("messageFollowers")
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    log_file_name = "ezselenium.lot"

    fh = logging.FileHandler(filename=log_file_name)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    LOGGER.addHandler(ch)
    LOGGER.addHandler(fh)

    driver = load_browser(
        "D:\\Documents\\ai-shirt-maker\\bot\\chromedrivers", headless=False)

    driver.quit()
