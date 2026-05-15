# Automation Challenge — saucedemo.com

## Stack
- Python 3 + Selenium 4 + pytest + pytest-html

## Estructura
```
├── conftest.py          ← fixture del browser + screenshot en fallo
├── pytest.ini           ← configuración pytest
├── requirements.txt
├── test_cases.md        ← casos de prueba escritos
└── tests/
    ├── test_login.py    ← 4 tests de login (1 falla intencional)
    ├── test_cart.py     ← 4 tests del carrito
    └── test_api.py      ← 2 tests API Mercado Libre
```

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
```bash
# Chrome (por defecto)
pytest

# Firefox
pytest --browser=firefox

# Solo un archivo
pytest tests/test_login.py
```

## Reporte
Se genera en `reports/report.html` después de cada ejecución.  
Las capturas de pantalla de fallos se guardan en `reports/screenshots/`.

