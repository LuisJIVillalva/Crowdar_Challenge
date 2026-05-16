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
from locators.login_locators import INPUT_USERNAME, INPUT_PASSWORD, BUTTON_LOGIN, ERROR_MESSAGE


class TestData:
    productive_unit = None
    case_name = f"{os.path.basename(__file__)[:-3]}"
    username = read_config_file("USERS", "locked_out_user")
    password = read_config_file("USERS", "locked_out_user_pass")
    base_url = read_config_file("WEB", "base_url")
    browser = read_config_file("WEB", "browser")
    headless =  True if read_config_file("WEB", "headless").upper() == "TRUE" else False
    error_locked_out_user = read_config_file("ERROR_MESSAGES", "locked_out_user")
    error_user_required = read_config_file("ERROR_MESSAGES", "user_required")
    error_password_required = read_config_file("ERROR_MESSAGES", "password_required")
    error_password_incorrect = read_config_file("ERROR_MESSAGES", "password_incorrect")
    headers = None
    video = None
    wd = None


@pytest.mark.login
@pytest.mark.parametrize(("case_name", "user", "password", "expected_error"),
                         (("Usuario bloqueado", TestData.username, TestData.password, TestData.error_locked_out_user),
                         ("Contraseña incorrecta", TestData.username, "pass_incorrect", TestData.error_password_incorrect),
                         ("Usuario incorrecto", "user_incorrect", TestData.password, TestData.error_password_incorrect),
                         ("No se ingresa contraseña", TestData.username, "",TestData.error_password_required),
                         ("No se ingresa usuario", "", TestData.password, TestData.error_user_required),
                         ("No se ingresa usuario ni contraseña","", "", TestData.error_user_required)),
                         ids=["1:usuario_bloqueado",
                              "2:contrasenia_incorrecta",
                              "3:usuario_incorrecto",
                              "4:No_se_ingresa_contrasenia",
                              "5:No_se_ingresa_usuario",
                              "6:No_se_ingresa_usuario_ni_contrasenia"
                              ])
def test_login_negative(case_name, user, password, expected_error):
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

        log.info(f"Esperando el error: {expected_error}")
        WebDriverWait(TestData.wd, 10).until(
            ec.text_to_be_present_in_element(resolve_locator(ERROR_MESSAGE), expected_error))

    except BaseException as err:
        raise Exception("Hubo un error - {}".format(str(err).replace('\n', ' ')))
    finally:
        if sys.exc_info()[0] is None:
            unregister_driver(TestData.case_name)
            if TestData.wd:
                TestData.wd.quit()
