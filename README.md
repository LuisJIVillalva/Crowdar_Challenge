# Automation Challenge — saucedemo.com

## Stack
- Python 3.10+ · Selenium 4 · pytest · pytest-html · requests · jsonschema

---

## Estructura del proyecto
```
├── config/
│   └── config_sit.ini       ← configuración de entorno (URLs, usuarios, browser)
├── core/
│   ├── browser.py           ← factory del WebDriver
│   ├── envs.py              ← lectura del config .ini
│   ├── functions.py         ← cliente HTTP (requests)
│   ├── locator_utils.py     ← resolución de locators
│   └── logging_local.py     ← logger
├── locators/                ← locators por pantalla
├── schemas/
│   └── backend/             ← JSON schemas para validar responses
├── tests/
│   ├── backend/             ← tests de API (Mercado Libre)
│   └── frontend/
│       ├── login/           ← tests de inicio de sesión
│       └── shopping_cart/   ← tests del carrito de compras
├── utils/
│   ├── endpoint_list.py     ← lista de endpoints
│   └── web_utils.py         ← helpers web (login, post_case_execution)
├── reports/
│   ├── report.html          ← reporte generado automáticamente
│   └── screenshots/         ← capturas de pantalla en caso de fallo
├── conftest.py              ← hooks de pytest (screenshot en fallo)
├── pytest.ini               ← configuración de pytest
└── requirements.txt
```

---

## Requisitos previos

- **Python 3.10 o superior** → https://www.python.org/downloads/
  > ⚠️ Usar el instalador **Windows installer (64-bit)** — *standalone installer*. Durante la instalación activar el checkbox **"Add Python to PATH"**.
- **Google Chrome** (versión reciente) → https://www.google.com/chrome/
- **Firefox** (opcional) → https://www.mozilla.org/firefox/

Verificá que Python esté instalado correctamente:
```bash
python --version
```

---

## Instalación

### Opción A — Automática (recomendada)

El proyecto incluye dos scripts `.bat` para CMD que automatizan la configuración:

**Primera vez** (instala todo y deja la consola lista):
```cmd
configure_tool.bat
```

**Consolas siguientes** (activa el entorno y configura las variables):
```cmd
configure_env.bat
```

Al terminar ambos scripts, la consola queda con `(crowdar_env)` activo y las variables configuradas, lista para ejecutar `pytest`.

---

### Opción B — Manual (si los scripts fallan)

> Los siguientes comandos están escritos para **CMD (Símbolo del sistema)**.  
> Si usás **PowerShell**, cambiá `.\crowdar_env\Scripts\activate.bat` por `.\crowdar_env\Scripts\Activate.ps1`  
> y `set BIZ_AUTOMATION_ENV=...` por `$env:BIZ_AUTOMATION_ENV = "..."`.

#### 1. Clonar el repositorio
```cmd
git clone <URL_DEL_REPOSITORIO>
cd PythonProject
```

#### 2. Instalar virtualenv
```cmd
pip install virtualenv
```

#### 3. Crear el entorno virtual
```cmd
virtualenv -p "C:\RutaDePython\python.exe" crowdar_env
```
> ⚠️ Reemplazá `C:\RutaDePython\python.exe` por la ruta real donde instalaste Python.  
> Para encontrarla ejecutá: `where python`

#### 4. Activar el entorno virtual
```cmd
.\crowdar_env\Scripts\activate.bat
```
Una vez activo, el prompt muestra `(crowdar_env)` al inicio.

#### 5. Actualizar pip e instalar dependencias
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Configurar variable de entorno
```cmd
set BIZ_AUTOMATION_ENV=config/config_sit.ini
```

> ⚠️ **Los pasos 4 y 6 deben repetirse cada vez que se abre una consola nueva.**  
> El entorno virtual y las variables no persisten entre sesiones.  
> O simplemente ejecutá `configure_env.bat` para hacerlo automáticamente.

---

## Configuración

El archivo `config/config_sit.ini` contiene todos los parámetros configurables:

```ini
[WEB]
base_url = https://www.saucedemo.com
browser  = chrome      # chrome | firefox
headless = false       # true | false

[BACKEND]
host = https://www.mercadolibre.com.ar/
```

Para correr en **Firefox** cambiá `browser = firefox`.  
Para correr **sin ventana** (CI/CD) cambiá `headless = true`.

### Múltiples ambientes

El proyecto soporta distintos archivos de configuración por ambiente. Ya incluye:

```
config/
├── config_sit.ini   ← SIT (por defecto)
└── config_uat.ini   ← UAT
```

Para cambiar de ambiente tenés dos opciones:

**Opción 1 — Editar `configure_env.bat`** (una sola vez):
```bat
:: Cambiá esta línea por el archivo del ambiente deseado
set BIZ_AUTOMATION_ENV=config/config_uat.ini
```

**Opción 2 — Ejecutar manualmente en CMD**:
```cmd
:: SIT
set BIZ_AUTOMATION_ENV=config/config_sit.ini

:: UAT
set BIZ_AUTOMATION_ENV=config/config_uat.ini
```

> Para agregar un nuevo ambiente simplemente creá un nuevo archivo `config/config_<nombre>.ini` siguiendo la misma estructura y apuntá la variable a ese archivo.

---

## Ejecución de tests

```bash
# Todos los tests
pytest

# Solo tests de login
pytest tests/frontend/login/

# Solo tests del carrito
pytest tests/frontend/shopping_cart/

# Solo tests de API
pytest tests/backend/

# Un archivo específico
pytest tests/frontend/login/test_login.py

# Con detalle y logs en consola
pytest -v -s
```

---

## Reporte

Después de cada ejecución se genera automáticamente:

- **`reports/report.html`** → reporte completo con logs y capturas de pantalla
- **`reports/screenshots/`** → imágenes `.png` de los tests fallidos

Para abrirlo, hacé doble click en `reports/report.html` o abrilo desde el navegador.

---

## Casos de prueba documentados

Los casos de prueba están documentados en dos formatos dentro de la carpeta `test_cases/`:

- **`test_cases/login.feature`** → escenarios de inicio de sesión en formato Gherkin
- **`test_cases/shopping_cart.feature`** → escenarios del carrito de compras en formato Gherkin

> ⚠️ **Nota:** los archivos `.feature` son únicamente documentación de los casos a automatizar.
> **No se implementó BDD** (Behave / pytest-bdd). Las pruebas automatizadas se encuentran directamente en la carpeta `tests/` usando pytest.
