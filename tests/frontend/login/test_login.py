import os
import sys

import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from core.browser import get_driver
from core.envs import read_config_file
from core.locator_utils import resolve_locator
from conftest import register_driver, unregister_driver
from core.logging_local import log
from locators.home_locators import BUGER_MENU
from locators.login_locators import INPUT_USERNAME, INPUT_PASSWORD, BUTTON_LOGIN


class TestData:
    case_name = f"{os.path.basename(__file__)[:-3]}"
    username = read_config_file("USERS", "user")
    password = read_config_file("USERS", "user_pass")
    base_url = read_config_file("WEB", "base_url")
    browser = read_config_file("WEB", "browser")
    headless =  True if read_config_file("WEB", "headless").upper() == "TRUE" else False
    headers = None
    video = None
    wd = None


@pytest.mark.login
def test_login():
    try:
        TestData.wd = get_driver(TestData.base_url, browser=TestData.browser, headless=TestData.headless)
        register_driver(TestData.case_name, TestData.wd)

        log.info("Ingresando usuario")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(INPUT_USERNAME))).send_keys(TestData.username)

        log.info("Ingresando password")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(INPUT_PASSWORD))).send_keys(TestData.password)

        log.info("Haciendo click en el botón de login")
        WebDriverWait(TestData.wd, 10).until(
            ec.element_to_be_clickable(resolve_locator(BUTTON_LOGIN))).click()

        log.info("Esperando el menu hamburguesa")
        WebDriverWait(TestData.wd, 10).until(
            ec.element_to_be_clickable(resolve_locator(BUGER_MENU)))

    except BaseException as err:
        raise Exception("Hubo un error - {}".format(str(err).replace('\n', ' ')))
    finally:
        if sys.exc_info()[0] is None:
            unregister_driver(TestData.case_name)
            if TestData.wd:
                TestData.wd.quit()
