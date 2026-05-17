from selenium import webdriver as selenium_webdriver
from selenium.common.exceptions import WebDriverException


def get_driver(url: str, browser: str = "chrome", headless: bool = False):
    """
    Crea un driver, abre la URL indicada y lo retorna.
    Usa Selenium Manager (integrado en Selenium 4.6+), sin webdriver-manager.

    Parámetros:
        url      : URL a abrir al iniciar el driver
        browser  : "chrome" (por defecto) | "firefox"
        headless : True para correr sin ventana, False para verla (por defecto False)

    Uso:
        driver = get_driverurl("https://www.saucedemo.com")
        driver = get_driverurl("https://www.saucedemo.com", browser="firefox")
        driver = get_driverurl("https://www.saucedemo.com", headless=True)
    """
    browser = browser.lower().strip()

    if browser == "firefox":
        options = selenium_webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = selenium_webdriver.Firefox(options=options)

    else:  # chrome por defecto
        options = selenium_webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        driver = selenium_webdriver.Chrome(options=options)

    driver.maximize_window()

    try:
        driver.get(url)
    except WebDriverException as e:
        driver.quit()
        raise WebDriverException(f"No se pudo abrir la URL '{url}': {e}")

    return driver
