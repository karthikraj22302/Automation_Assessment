import csv
import os
from datetime import datetime
import pytest
from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from Citpl_Fw.SeleniumBase import ClsSeleniumBase as sb
from Application.Resources.Input.Env_properties import ClsEnvProperties as env, ClsEnvProperties

test_results_file_name = "test_results.csv"

browser_to_execute = ""

GET_TEST_DATA = {}

# ---------------------- PYTEST CUSTOMIZATION SECTION ----------------------


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Choose browser: chrome, edge, ff, safari")

# Fixture to get browser from command line
@pytest.fixture(scope='module')
def browser(request):
    return request.config.getoption("--browser")

# Main setup/teardown fixture for each test
@pytest.fixture(scope="function")
def setup_and_tear_down(browser):
    wd = None
    if browser == 'chrome':
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--incognito")  # Run Chrome in incognito mode
        wd = webdriver.Chrome(options=chrome_options)
    elif browser == 'edge':
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-gpu")
        wd = webdriver.Edge(options=edge_options)
    elif browser == 'safari':
        wd = webdriver.Safari()
    elif browser == 'ff':
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("layers.acceleration.disabled", True)  # Disable GPU
        wd = webdriver.Firefox(options=firefox_options)

    yield wd  # Provide driver to test
    wd.quit()  # Close browser after test


# ---------------------- CSV FILE MANAGEMENT FIXTURE ----------------------

# Setup/teardown for CSV logging
@pytest.fixture(scope='module', autouse=True)
def csv_file_setup(request):
    csv_file_path = env.get_test_results_file()
    results = []  # Store test results in memory

    yield results  # Provide it to tests

    # If CSV doesn't exist, create and write header
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tests Case Name', 'Status', 'Duration'])
            writer.writerows(results)
    else:
        # If exists, just append new results
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(results)

    # Optional cleanup after all tests
    def teardown():
        pass

    request.addfinalizer(teardown)
    return csv_file_path

# ---------------------- UTILITY FIXTURES ----------------------

# This fixture is used to store any additional test-specific data
@pytest.fixture(scope='module')
def store_test_data(request):
    print(f"Fixture received: {request.param}")
    return request.param

# Attach extra info to test cases
@pytest.fixture
def get_additional_test_case_info(request):
    request.node.get_additional_test_case_info = {}
    return request.node.get_additional_test_case_info

# ---------------------- PYTEST HOOK FOR RESULT TRACKING ----------------------

# This hook gets called after each test execution
@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(report):
    SCREENSHOT_NAME = ""
    GENERATED_SCREENSHOT_PATH = ""
    test_status_to_write_in_csv = []

    if report.when == "call":  # Run after test case executed

        # Getting module and test details
        module = getattr(report, 'get_additional_test_case_info', {}).get('module', 'N/A')
        test_case_name = sb.split_string(report.nodeid, "::", 1)

        if report.outcome == 'failed':
            SCREENSHOT_NAME = test_case_name + sb.get_current_date("_%Y_%m_%d_") + sb.get_current_time("%H_%M_%S")
            GENERATED_SCREENSHOT_PATH = take_screenshot(SCREENSHOT_NAME, "jpeg", 5)

        # Tests metadata
        test_date = sb.get_current_date("%Y-%m-%d")
        test_time = sb.get_current_time("%H:%M:%S")
        project_name = env.PROJECT_NAME
        duration = sb.round_decimal(report.duration, 2)

        # Write test result to CSV
        test_status_to_write_in_csv.extend([
            test_date, test_time, browser_to_execute, project_name,
            module, "", test_case_name, report.outcome, duration, GENERATED_SCREENSHOT_PATH
        ])
        write_into_csv(test_status_to_write_in_csv)

        # Write to DB (optional)
        test_status_to_write_in_db = {
            "browser": browser_to_execute,
            "project": project_name,
            "module": module,
            "sub_module": "",
            "test_case_name": test_case_name,
            "status": report.outcome,
            "duration": duration,
            "screenshot": "",
            "timestamp": datetime.now(),
            "date": "",
            "time": ""
        }
        # write_into_db(test_status_to_write_in_db)

# ---------------------- CSV AND DB UTILITIES ----------------------

# Function to write data into CSV
def write_into_csv(results):
    csv_file_path = env.get_test_results_file()
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Time', 'Browser', 'Project', 'Module', 'Sub_Module', 'Test_Case_Name', 'Status', 'Duration', 'Screenshot'])
            writer.writerow(results)
    else:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(results)


# ---------------------- SCREENSHOT FUNCTION ----------------------

# Takes screenshot and saves in given format
def take_screenshot(test_name, file_extn, quality):
    screenshot_dir = os.path.join(ClsEnvProperties.get_base_dir_path(), "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")

    try:
        screenshot = ImageGrab.grab()  # Capture full screen
        if file_extn == "jpeg":
            screenshot.save(screenshot_path, "JPEG", quality=quality)
        elif file_extn == "png":
            screenshot.save(screenshot_path, "PNG")

        print(f"Screenshot saved at {screenshot_path}")
        return screenshot_path
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None


