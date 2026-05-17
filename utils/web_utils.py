from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from conftest import unregister_driver
from core.browser import get_driver
from core.envs import read_config_file
from core.locator_utils import resolve_locator
from core.logging_local import log
from locators.login_locators import INPUT_USERNAME, INPUT_PASSWORD, BUTTON_LOGIN

base_url = read_config_file("WEB", "base_url")
browser = read_config_file("WEB", "browser")
headless = True if read_config_file("WEB", "headless").upper() == "TRUE" else False

def login(user, password):
    log.info("Iniciando sesión en la aplicación")
    wd = get_driver(base_url, browser=browser, headless=headless)

    log.info("Ingresando usuario")
    WebDriverWait(wd, 10).until(
        ec.presence_of_element_located(resolve_locator(INPUT_USERNAME))).send_keys(user)

    log.info("Ingresando password")
    WebDriverWait(wd, 10).until(
        ec.presence_of_element_located(resolve_locator(INPUT_PASSWORD))).send_keys(password)

    log.info("Haciendo click en el botón de login")
    WebDriverWait(wd, 10).until(
        ec.element_to_be_clickable(resolve_locator(BUTTON_LOGIN))).click()

    return wd



def post_case_execution_web(wd, status_ok, case_name):
    try:
        if status_ok:
            unregister_driver(case_name)
            if wd:
                wd.quit()
    except BaseException as err:
        log.warning(f"Hubo un error en post_case_execution: {err}")
