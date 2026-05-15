from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


def resolve_locator(locator):
    """
       Resuelve una cadena de localización en una tupla del tipo de localizador y el valor del localizador.

       Args:
           locator str: La cadena de localización en formato 'tipo:valor'.

       Returns:
           tuple[str, str]: Una tupla que contiene el tipo de localizador (por ejemplo, 'ID') y el valor del localizador.

       Ejemplo:
           resolve_locator('id:mi_elemento') -> (AppiumBy.ID, 'mi_elemento')
       """
    locator_type, locator = locator.split(":", 1)
    if hasattr(AppiumBy, locator_type):
        return getattr(AppiumBy, locator_type.upper()), locator
    elif hasattr(By, locator_type.upper()):
        return getattr(By, locator_type.upper()), locator
    else:
        raise ValueError(f"El locator_type '{locator}' no es válido.")
