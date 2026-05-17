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
    from core.browser import get_driver
    name = request.config.getoption("--browser")
    driver = get_driver(name)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        matched_key = None

        if not driver:
            if item.name in _active_drivers:
                matched_key = item.name
                driver = _active_drivers[matched_key]

        if not driver:
            for key in _active_drivers:
                if item.name.startswith(key):
                    matched_key = key
                    driver = _active_drivers[key]
                    break

        if driver:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = item.name.replace("[", "_").replace("]", "").replace(":", "_").replace("/", "_").replace("\\", "_")
                filename = f"{safe_name}_{timestamp}.png"
                path = os.path.join(SCREENSHOTS_DIR, filename)
                driver.save_screenshot(path)

                if pytest_html:
                    from pytest_html import extras as html_extras
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode("utf-8")
                    img_src = f"data:image/png;base64,{encoded}"
                    extra.append(html_extras.html(
                        f'<div style="margin-top:10px">'
                        f'<p><b>📸 Screenshot al momento del fallo:</b></p>'
                        f'<img src="{img_src}" style="max-width:800px;width:100%;border:1px solid #ccc;border-radius:4px"/>'
                        f'</div>'
                    ))
                    report.extras = extra

            except Exception as e:
                print(f"\n⚠️  Error en screenshot: {e}")
                import traceback
                traceback.print_exc()
            finally:
                if matched_key and matched_key in _active_drivers:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    _active_drivers.pop(matched_key, None)
