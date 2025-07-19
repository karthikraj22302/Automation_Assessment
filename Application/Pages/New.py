import os
import time

import pyautogui
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from Application.Pages.Po_Login import Cls_Po_Login

class Locators_New():
    REGISTER="//i[@class='icon-user']"
    PATIENT_NAME="//input[@name='givenName']"
    MIDDLE_NMAE="//input[@name='middleName']"
    FAMILY_NAME="//input[@name='familyName']"
    RIGHT_NEXT_BTN="//button[@class='confirm right']"
    GENDER_MALE="//option[text()='Male']"
    GENDER_FEMALE="//option[text()='Female']"
    BDAY="//input[@id='birthdateDay-field']"
    BMONTH="//select[@id='birthdateMonth-field']"
    BYEAR="//input[@id='birthdateYear-field']"
    ADDRESS="//input[@id='address1']"
    CITY="//input[@id='cityVillage']"
    STATE="//input[@id='stateProvince']"
    COUNTRY="//input[@id='country']"
    POSTAL_CODE="//input[@id='postalCode']"
    PHONE_NO="//input[@name='phoneNumber']"
    # verfication
    VER_NAME="//span[text()='Name']/preceding-sibling::i[contains(@class,'icon-ok')]"
    VER_GENDER="//span[text()='Gender']/preceding-sibling::i[contains(@class,'icon-ok')]"
    VER_BRITH="//span[text()='Birthdate']/preceding-sibling::i[contains(@class,'icon-ok')]"
    VER_PHONE="//span[text()='Phone Number']/preceding-sibling::i[contains(@class,'icon-ok')]"
    VER_ADDRESS="//span[text()='Address']/preceding-sibling::i[contains(@class,'icon-ok')]"
    #
    CONFIRM_BTN="//input[@id='submit']"
    VER_DETAILS_PAGE="//span[text()='Show Contact Info']"
    START_VISIT_BTN="//div[contains(text(),'Start Visit')]"
    VISIT_CONFIRM_BTN="//button[@id='start-visit-with-visittype-confirm']"
    # Attachement
    ATTACHMENT_BTN="//a[@id='attachments.attachments.visitActions.default']"
    UPLOAD_BTN="//form[@id='visit-documents-dropzone']"
    CAPTION_TXT="//h3[text()='Caption']/following-sibling::textarea"
    IMG_UPLOAD_BTN="//button[text()='Upload file']"
    ATTACH_POP_MSG="//p[text()='The attachment was successfully uploaded.']"
    END_VISIT="//h3[text()='ALLERGIES']/parent::div/parent::div/parent::div/parent::div/parent::div//following-sibling::div/child::div/child::ul/child::li[@class='float-left']/child::a[@id='referenceapplication.realTime.endVisit']"
    END_YES_BTN="//span[text()='Are you sure you want to end this visit?']/ancestor::div//button[text()='Yes']"
    # delete
    DELETE_BTN="//div[contains(text(),'Delete Patient')]"
    DELETE_TXT="//input[@id='delete-reason']"
    DELETE_CONFIRM_BTN="//input[@id='delete-reason']/parent::div/child::button[text()='Confirm']"
    DELETE_POP_MSG="//p[text()='Patient has been deleted successfully']"
    PATIENT_TABLE="//input[@id='patient-search']"

class Cls_new(Cls_Po_Login):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def Assement(self,Name,M_Name,F_Name,Bday,byear,Address,City,State,Phone_No):
        #Verify dashboard page is redirected using Assertion
        self.assert_condition(self.is_element_visible("xpath",Locators_New.REGISTER),
                              "Dashboard page is visible after login.",
                              "Dashboard page is not visible after login.")
        #Click on Register a patent menu.
        self.click("xpath",Locators_New.REGISTER)
        self.driver.implicitly_wait(10)
        # Enter the detail of Demographics(Name, Gender, Birthdate) and Contact Info(Address, Phone number)
        self.enter_text("xpath",Locators_New.PATIENT_NAME,Name)
        Name_find=Name
        self.enter_text("xpath",Locators_New.MIDDLE_NMAE,M_Name)
        self.enter_text("xpath",Locators_New.FAMILY_NAME,F_Name)
        self.click("xpath",Locators_New.RIGHT_NEXT_BTN)
        self.click("xpath",Locators_New.GENDER_MALE)
        self.click("xpath",Locators_New.RIGHT_NEXT_BTN)
        self.enter_text("xpath",Locators_New.BDAY,Bday)
        dropdown = Select(self.driver.find_element("xpath",Locators_New.BMONTH))
        dropdown.select_by_visible_text("March")
        self.enter_text("xpath",Locators_New.BYEAR,byear)
        self.click("xpath", Locators_New.RIGHT_NEXT_BTN)
        self.enter_text("xpath",Locators_New.ADDRESS,Address)
        self.enter_text("xpath",Locators_New.CITY,City)
        self.enter_text("xpath",Locators_New.STATE,State)
        self.enter_text("xpath",Locators_New.COUNTRY,"INDIA")
        self.enter_text("xpath",Locators_New.POSTAL_CODE,"123456")
        self.click("xpath", Locators_New.RIGHT_NEXT_BTN)
        self.enter_text("xpath",Locators_New.PHONE_NO,Phone_No)
        self.click("xpath", Locators_New.RIGHT_NEXT_BTN)
        self.driver.implicitly_wait(10)
        # Then at Confirm page, verify the given Name, Gender, Birthdate, Address, and Phone number are populated correctly using Assertion
        self.assert_condition(self.is_element_visible("xpath", Locators_New.VER_NAME),"Name step  completed","Name step not completed")
        self.assert_condition(self.is_element_visible("xpath", Locators_New.VER_GENDER), "Gender step completed","Gender step not completed")
        self.assert_condition(self.is_element_visible("xpath", Locators_New.VER_BRITH), "brith step completed","birth step not completed")
        self.assert_condition(self.is_element_visible("xpath", Locators_New.VER_ADDRESS), "Address step completed","Address step not completed")
        self.assert_condition(self.is_element_visible("xpath", Locators_New.VER_PHONE), "Phone step completed","phone step not completed")
        # Click on Confirm and verify Patient details page is redirected.
        self.click("xpath", Locators_New.RIGHT_NEXT_BTN)
        self.click("xpath",Locators_New.CONFIRM_BTN)
        self.driver.implicitly_wait(10)
        self.assert_condition(self.is_element_visible("xpath", Locators_New.VER_DETAILS_PAGE)," Patient Details page is displayed after confirming registration."," Failed to navigate to Patient Details page after clicking Confirm.")
        # Click on Start Visit and Confirm the visit.
        self.click("xpath",Locators_New.START_VISIT_BTN)
        self.click("xpath",Locators_New.VISIT_CONFIRM_BTN)
        #Click on Attachment and complete the upload process
        self.click("xpath",Locators_New.ATTACHMENT_BTN)
        time.sleep(5)
        #file upload
        self.click("xpath", Locators_New.UPLOAD_BTN)
        current_directory = os.getcwd()
        project_root = current_directory
        while not os.path.isdir(os.path.join(project_root, 'Application')):
            project_root = os.path.dirname(project_root)
            if project_root == os.path.dirname(project_root):
                raise Exception("Project root directory with 'Application' not found")
        # Construct File Path:
        file_path = os.path.join(project_root, "Application","Resources", "Input", "Image.jpg")
        absolute_path = os.path.abspath(file_path)
        if not os.path.isfile(absolute_path):
            raise FileNotFoundError(f"File not found: {absolute_path}")
        print(absolute_path)
        pyperclip.copy(absolute_path)
        self.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        self.sleep(1)
        pyautogui.press('enter')
        self.enter_text("xpath",Locators_New.CAPTION_TXT,"Automation_testing")
        self.click("xpath",Locators_New.IMG_UPLOAD_BTN)
        #Verify toaster message appeared for the successful attachment
        self.assert_condition(self.is_element_visible("xpath",Locators_New.ATTACH_POP_MSG),"Attachment uploaded successfully."
                              ,"Attachment failed. Please try again.")
        self.driver.implicitly_wait(10)
        print("Name_find is:", Name_find)
        #Redirect to the Patient details screen(its fail case iam using another type redirect)
        self.click_by_jse(By.XPATH, f"//a[contains(text(), '{Name_find}')]")
        self.driver.implicitly_wait(10)
        #Click on the End Visit action at RHS.
        self.click("xpath",Locators_New.END_VISIT)
        self.click("xpath", Locators_New.END_YES_BTN)
        time.sleep(5)
        #Click on Delete Patient and provide the reason
        self.click("xpath", Locators_New.DELETE_BTN)
        self.enter_text("xpath",Locators_New.DELETE_TXT,"Automation_testing")
        self.click("xpath",Locators_New.DELETE_CONFIRM_BTN)
        #Click on confirm button and verify the toaster message
        self.assert_condition(self.is_element_visible("xpath", Locators_New.DELETE_POP_MSG),
                              "Patient has been deleted successfully Displayed"
                              , "Patient has been NOT  deleted successfully Displayed")
        #It will redirect you to the Find Patient Record menu where verify the deleted patient should not be listed in the table using search options
        self.enter_text("xpath",Locators_New.PATIENT_TABLE,Name_find)
        patient_rows = self.driver.find_elements(By.XPATH, "//table[@id='patient-search-results-table']//td[1]")
        patient_found = False
        for row in patient_rows:
            if Name_find.lower() in row.text.lower():
                patient_found = True
                break
        if not patient_found:
            print("Deleted patient is not listed – Test Passed")
        else:
            raise AssertionError(f"Test Failed: Deleted patient '{Name_find}' is still listed in the table")
        time.sleep(2)



