import os
import time

import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from core.browser import get_driver
from core.envs import read_config_file
from core.locator_utils import resolve_locator
from conftest import register_driver
from core.logging_local import log
from locators.home_locators import BUGER_MENU, BUTTON_ADD_TO_CART
from locators.login_locators import INPUT_USERNAME, INPUT_PASSWORD, BUTTON_LOGIN
from utils.web_utils import post_case_execution_web


class TestData:
    case_name = f"{os.path.basename(__file__)[:-3]}"
    username = read_config_file("USERS", "user")
    password = read_config_file("USERS", "user_pass")
    problem_user = read_config_file("USERS", "problem_user")
    problem_user_password = read_config_file("USERS", "problem_user_pass")
    performance_glitch_user = read_config_file("USERS", "performance_glitch_user")
    performance_glitch_user_pass = read_config_file("USERS", "performance_glitch_user_pass")
    error_user = read_config_file("USERS", "error_user")
    error_user_pass = read_config_file("USERS", "error_user_pass")
    visual_user = read_config_file("USERS", "visual_user")
    visual_user_pass = read_config_file("USERS", "visual_user_pass")
    base_url = read_config_file("WEB", "base_url")
    browser = read_config_file("WEB", "browser")
    headless = True if read_config_file("WEB", "headless").upper() == "TRUE" else False
    headers = None
    video = None
    wd = None


@pytest.mark.parametrize(("user", "password"),

                         ((TestData.username, TestData.password),
                          (TestData.problem_user, TestData.problem_user_password),
                          (TestData.performance_glitch_user, TestData.performance_glitch_user_pass),
                          (TestData.error_user, TestData.error_user_pass)),
                         ids=["1:usuario_standard",
                              "2:usuario_con_problemas",
                              "3:usuario_lento",
                              "4:usuario_error"
                              ])
def test_login(user, password):
    try:
        TestData.wd = get_driver(TestData.base_url, browser=TestData.browser, headless=TestData.headless)
        register_driver(TestData.case_name, TestData.wd)

        log.info("Ingresando usuario")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(INPUT_USERNAME))).send_keys(user)

        log.info("Ingresando password")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(INPUT_PASSWORD))).send_keys(password)

        log.info("Haciendo click en el botón de login")
        WebDriverWait(TestData.wd, 10).until(
            ec.element_to_be_clickable(resolve_locator(BUTTON_LOGIN))).click()

        log.info("Esperando la carga del inventario")
        WebDriverWait(TestData.wd, 1).until(
            ec.presence_of_element_located(resolve_locator(BUTTON_ADD_TO_CART))).click()


        post_case_execution_web(TestData.wd, True, TestData.case_name)
    except BaseException as err:
        post_case_execution_web(TestData.wd, False, TestData.case_name)
        raise Exception("Hubo un error - {}".format(str(err).replace('\n', ' ')))
