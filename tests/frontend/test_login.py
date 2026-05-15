import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from core.browser import get_driver
from core.locator_utils import resolve_locator
from conftest import register_driver, unregister_driver


class TestData:
    productive_unit = None
    headers = None
    video = None
    wd = None




@pytest.mark.login
def test_cambio_de_contrasenia():
    import sys
    try:
        TestData.wd = get_driver("https://www.youtube.com/", browser="chrome", headless=False)
        register_driver("test_cambio_de_contrasenia", TestData.wd)

        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator("ID:guide-iconn"))).click()

    except BaseException as err:
        raise Exception("Hubo un error - {}".format(str(err).replace('\n', ' ')))
    finally:
        # Solo cerramos el driver si el test pasó (sin excepción activa)
        # Si falló, el hook de conftest toma el screenshot y cierra el driver
        if sys.exc_info()[0] is None:
            unregister_driver("test_cambio_de_contrasenia")
            if TestData.wd:
                TestData.wd.quit()
