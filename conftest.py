import os
import base64
import pytest
from datetime import datetime

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")

_active_drivers = {}


def register_driver(test_name, driver):
    """Registra un driver para que el hook de screenshot lo encuentre al fallar."""
    _active_drivers[test_name] = driver


def unregister_driver(test_name):
    """Elimina el registro del driver al finalizar el test."""
    _active_drivers.pop(test_name, None)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser: chrome | firefox")


def pytest_configure(config):
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "reports"), exist_ok=True)


@pytest.fixture()
def browser(request):
    """
    Fixture que crea y cierra el driver automáticamente.
    Úsalo en tests que no manejen su propio driver:
        def test_algo(browser):
            browser.get("https://...")
    """
    from core.browser import get_driver
    name = request.config.getoption("--browser")
    driver = get_driver(name)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser") or _active_drivers.get(item.name)

        if driver:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{item.name}_{timestamp}.png"
                path = os.path.join(SCREENSHOTS_DIR, filename)
                driver.save_screenshot(path)

                try:
                    from pytest_html import extras
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode("utf-8")
                    report.extra = getattr(report, "extra", [])
                    report.extra.append(extras.html(
                        f'<div style="margin-top:10px">'
                        f'<p><b>📸 Screenshot al momento del fallo:</b></p>'
                        f'<img src="data:image/png;base64,{encoded}" '
                        f'style="max-width:50%;border:1px solid #ccc;border-radius:4px"/>'
                        f'</div>'
                    ))
                except Exception:
                    pass

                print(f"\n📸 Screenshot guardado: {path}")
            except Exception as e:
                print(f"\n⚠️  No se pudo tomar screenshot: {e}")
            finally:
                if item.name in _active_drivers:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    _active_drivers.pop(item.name, None)

