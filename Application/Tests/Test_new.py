import time
from Citpl_Fw import PyBase
from Application.Pages.Po_Login import Cls_Po_Login
from Application.Pages.New import Cls_new
from Application.Resources.Input.Env_properties import ClsEnvProperties as env
from conftest import setup_and_tear_down

def test_new_1(setup_and_tear_down):
    driver = setup_and_tear_down
    test_case_id = "test_01"
    tdd = PyBase.get_input_test_data(test_case_id, env.get_parent_dir_path())
    Cls_Po_Login(driver).login(tdd.get("username"), tdd.get("password"),tdd.get("dept"))
    Cls_new(driver).Assement(tdd.get("Name"),tdd.get("M_Name"),tdd.get("F_Name"),tdd.get("Bday"),
                             tdd.get("byear"),tdd.get("Address"),tdd.get("City"),tdd.get("State"),tdd.get("Phone_No"))
    time.sleep(2)