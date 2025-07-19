from Citpl_Fw.SeleniumBase import ClsSeleniumBase
from Application.Resources.Input.Env_properties import ClsEnvProperties


class Cls_Po_Login(ClsSeleniumBase):

    USERNAME_XPATH = "//input[@name='username']"
    PASSWORD_ = "//input[@name='password']"
    LOCATION="//li[text()='Pharmacy']"
    CLICK_SIGN_IN = "//input[@id='loginButton']"


    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.cls_Env_Properties = ClsEnvProperties()

        self.url = self.cls_Env_Properties.URL
        self.username = self.cls_Env_Properties.USERNAME
        self.password = self.cls_Env_Properties.PASSWORD

    def login(self, username, password,dept):
        ClsSeleniumBase.sleep(self, 3)
        self.driver.maximize_window()
        self.driver.get(self.url)

        ClsSeleniumBase.enter_text(self, "xpath", self.USERNAME_XPATH, username)
        ClsSeleniumBase.enter_text(self, "xpath", self.PASSWORD_, password)
        ClsSeleniumBase.click(self, "xpath", self.LOCATION)
        ClsSeleniumBase.click(self, "xpath", self.CLICK_SIGN_IN)

