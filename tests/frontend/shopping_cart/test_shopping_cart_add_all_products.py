import os

import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from conftest import register_driver
from core.envs import read_config_file
from core.locator_utils import resolve_locator
from core.logging_local import log
import locators.home_locators as home_locators
import locators.shopping_cart_locators as shopping_cart_locators
import locators.user_information_locators as user_information_locators
import locators.checkout_locators as checkout_locators
from utils.web_utils import login, post_case_execution_web


class TestData:
    wd = None
    error_flow_desc: str = None
    username = read_config_file("USERS", "user")
    password = read_config_file("USERS", "user_pass")
    problem_user = read_config_file("USERS", "problem_user")
    problem_user_pass = read_config_file("USERS", "problem_user_pass")
    case_name = f"{os.path.basename(__file__)[:-3]}"

def setup_class(user, password):
    try:
        TestData.wd = login(user, password)
        register_driver(TestData.case_name, TestData.wd)
        return False

    except BaseException as err:
        TestData.error_flow_desc = "Hubo un error - {} --> {}".format(TestData.error_flow_desc,
                                                                      str(err).replace('\n', ' '))
        return True


@pytest.mark.parametrize(("user", "password"),
                         ((TestData.username, TestData.password),
                         (TestData.problem_user, TestData.problem_user_pass)),
                         ids=["1:usuario_1",
                              "2:usuario_2"
                              ])
def test_shopping_cart_add_all_products(user, password):
    """
    El objetivo de este test es agregar todos los productos al carrito y finalizar la compra.
    """
    log.test("El objetivo de este test es agregar todos los productos al carrito y finalizar la compra.")
    if setup_class(user, password):
        pytest.skip(reason=TestData.error_flow_desc)
    try:
        log.info("Obteniendo todos los productos.")
        items = WebDriverWait(TestData.wd, 10).until(ec.presence_of_all_elements_located(resolve_locator(home_locators.ITEMS_CONTAINER)))
        items_data = {}
        log.info("Validando que el carrito esté vacío")
        WebDriverWait(TestData.wd, 10).until(ec.invisibility_of_element(resolve_locator(home_locators.COUNT_CART_ITEM)))

        for i, item in enumerate(items, start=1):
            price = WebDriverWait(item, 10).until(ec.presence_of_element_located(resolve_locator(home_locators.ITEM_PRICE.format(i)))).text
            name = WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(home_locators.ITEM_NAME.format(i)))).text
            items_data[name.replace("", "_")] = price

            log.info(f"Agregando al carrito el producto {name}")
            WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(home_locators.BUTTON_ADD_TO_CART))).click()

            log.info(f"Validando que el carrito tenga {i} item(s)")
            WebDriverWait(TestData.wd, 10).until(ec.text_to_be_present_in_element(resolve_locator(home_locators.COUNT_CART_ITEM), str(i)))

        log.info("Finalizando Compra.")
        log.info("Click en el carrito.")
        WebDriverWait(TestData.wd, 10).until(presence_of_element_located(resolve_locator(home_locators.BUTTON_SHOPPING_CART))).click()

        log.info("Validando que el carrito tenga todos los productos agregados")
        log.info("Obteniendo todos los productos.")
        items = WebDriverWait(TestData.wd, 10).until(ec.presence_of_all_elements_located(resolve_locator(shopping_cart_locators.ITEMS_CART_CONTAINER)))
        assert len(items_data) == len(items)

        assert len(items) > 0, "No se encontraron productos en el carrito"

        validate_items = []
        for i in range(len(items)):
            name = WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(shopping_cart_locators.CART_ITEM_NAME.format(i+1)))).text
            key = name.replace("", "_")

            log.info(f"Validando el producto {name}")
            assert key in items_data, f"El producto {name} no se agregó en el carrito"

            log.info("Validando la cantidad del producto: 1")
            WebDriverWait(TestData.wd, 10).until(ec.text_to_be_present_in_element(resolve_locator(shopping_cart_locators.CART_QUANTITY.format(i+1)), "1"))

            log.info(f"Validando que el precio sea {items_data[key]}")
            WebDriverWait(TestData.wd, 10).until(ec.text_to_be_present_in_element(resolve_locator(shopping_cart_locators.CART_ITEM_PRICE.format(i+1)), items_data[key]))

            assert name not in validate_items, f"El producto {name} se encuentra repetido en el carrito"
            validate_items.append(name)

        #------------ El caso de prueba definido en el feature finalizaría acá, se continúa con la automatización hasta finalizar la compra ------------

        log.info("Click en el botón checkout")
        WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(shopping_cart_locators.BUTTON_CHECKOUT))).click()

        log.info("Ingresando datos del comprador")
        log.info("Ingresando nombre")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(user_information_locators.INPUT_NAME))).send_keys("Luis Juan Ignacio")
        log.info("Ingresando apellido")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(user_information_locators.INPUT_LAST_NAME))).send_keys("Villalva")
        log.info("Ingresando código postal")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(user_information_locators.INPUT_POSTAL_CODE))).send_keys("3400")

        log.info("Click en el botón continuar")
        WebDriverWait(TestData.wd, 10).until(
            ec.presence_of_element_located(resolve_locator(user_information_locators.BUTTON_CONTINUE))).click()

        log.info("Validando los totales")
        subtotal = 0
        for price_str in items_data.values():
            subtotal += float(price_str.replace("$", ""))

        log.info(f"Sub total esperado: {subtotal}")
        WebDriverWait(TestData.wd, 10).until(ec.text_to_be_present_in_element(resolve_locator(checkout_locators.SUBTOTAL_LABEL), f"${subtotal:.2f}"))

        tax = WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(checkout_locators.TAX_LABEL))).text
        tax = float(tax.replace("Tax: $", ""))
        total = subtotal + tax
        log.info(f"Total esperado: {total}")
        WebDriverWait(TestData.wd, 10).until(ec.text_to_be_present_in_element(resolve_locator(checkout_locators.TOTAL_LABEL), f"${total:.2f}"))

        log.info("Click en el botón Finish")
        WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(checkout_locators.BUTTON_FINISH))).click()

        log.info("Validando que se muestre el mensaje de compra finalizada")
        WebDriverWait(TestData.wd, 10).until(ec.text_to_be_present_in_element(resolve_locator(checkout_locators.FINISH_LABEL), "Thank you for your order!"))

        log.info("Validando que el carrito esté vacío")
        WebDriverWait(TestData.wd, 10).until(ec.invisibility_of_element(resolve_locator(home_locators.COUNT_CART_ITEM)))

        log.info("Volviendo a la home")
        WebDriverWait(TestData.wd, 10).until(ec.presence_of_element_located(resolve_locator(checkout_locators.BUTTON_BACK_HOME))).click()

        log.info("Validando que los productos no estén en el carrito")
        WebDriverWait(TestData.wd, 10).until(ec.invisibility_of_element(resolve_locator(home_locators.BUTTON_REMOVE)))

        post_case_execution_web(TestData.wd, True, TestData.case_name)
    except BaseException as err:
        log.error(f"Hubo un error durante la ejecución del test: {str(err).replace('\n', ' ')}")
        post_case_execution_web(TestData.wd, False, TestData.case_name)
        raise Exception("Hubo un error - {} --> {}".format(TestData.error_flow_desc, str(err).replace('\n', ' ')))
