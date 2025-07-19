import os
from Citpl_Fw.SeleniumBase import ClsSeleniumBase as sb

class ClsEnvProperties:
        PROJECT_NAME = "OpenMRS_Automation"
        PROJECT_ROOT_FOLDER_NAME = "/OpenMRS_Automation"
        URL = "https://demo.openmrs.org/openmrs/login.htm "
        USERNAME = "Admin"
        PASSWORD = "Admin123"
        CSV_FILE_PATH = "test_results.csv"
        TEST_DATE_FILE = PROJECT_ROOT_FOLDER_NAME + "/Application/Resources/Input/Test_Data_Excel.xlsx"
        TEST_RESULT_HTML_TEMPLATE_PATH = "/Input/test_result_template.html"
        TEST_RESULT_HTML_PATH = "/test_automation_results.html"

        @staticmethod
        def env_properties_qa():
            return {
                "customer": "OpenMRS_Automation",
                "env": "QA environment",
                "url": "https://demo.openmrs.org/openmrs/login.htm ",
                "username": "Admin",
                "password": "Admin123",
            }

        @staticmethod
        def get_test_results_file():
            test_result_file = str(
                os.path.join(ClsEnvProperties.get_reports_folder_path(), ClsEnvProperties.CSV_FILE_PATH))
            print("Tests result file is :: " + test_result_file)
            return test_result_file

        @staticmethod
        def get_project_root_folder_path():
            project_root = str(ClsEnvProperties.get_parent_dir_path())
            print("Project root folder name and path :: " + project_root)
            return project_root

        @staticmethod
        def get_html_template_path():
            template_path = str(
                ClsEnvProperties.get_project_root_folder_path() + ClsEnvProperties.TEST_RESULT_HTML_TEMPLATE_PATH)
            print("HTML template path :: " + template_path)
            return template_path

        @staticmethod
        def get_html_results_path():
            results_path = str(ClsEnvProperties.get_reports_folder_path() + ClsEnvProperties.TEST_RESULT_HTML_PATH)
            print("Automation test results HTML file path :: " + results_path)
            return results_path

        @staticmethod
        def get_reports_folder_path():
            # Get the reports folder path inside the framework directory (which is under the ClsEnvProperties root)
            framework_folder = ClsEnvProperties.get_project_root_folder_path()  # Use the framework root directory
            reports_folder = os.path.join(framework_folder, "Reports")

            # Create the folder if it doesn't exist
            sb.create_folder_if_not_exists(reports_folder)
            print("Reports folder path :: " + reports_folder)
            return reports_folder

        @staticmethod
        def get_base_dir_path():
            # Define the base directory as the framework folder where automation scripts exist
            framework_folder = ClsEnvProperties.get_project_root_folder_path()
            sb.create_folder_if_not_exists(framework_folder)

            print("Base directory for the framework folder: " + str(framework_folder))
            return str(framework_folder)

        @staticmethod
        def get_parent_dir_path():
            current_directory = os.path.dirname(os.path.abspath(__file__))
            parent_directory = os.path.dirname(current_directory)
            print("Current directory using os module:", current_directory)
            print("Parent directory using os module:", parent_directory)
            return str(parent_directory)