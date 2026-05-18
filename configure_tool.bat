@echo off
echo === Automation Challenge - Setup ===
echo.

echo [1/5] Instalando virtualenv...
pip install virtualenv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo instalar virtualenv. Verificar que Python este instalado y en el PATH.
    pause
    exit /b 1
)

echo [2/5] Detectando ruta de Python...
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
echo Python encontrado en: %PYTHON_PATH%

echo [3/5] Creando entorno virtual...
if exist crowdar_env (
    echo El entorno virtual ya existe, omitiendo creacion.
) else (
    virtualenv -p "%PYTHON_PATH%" crowdar_env
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
)

echo [4/5] Activando entorno e instalando dependencias...
call .\crowdar_env\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo [5/5] Setup completo.
echo.
echo === Abriendo consola lista para usar ===
cmd /k ".\crowdar_env\Scripts\activate.bat && set BIZ_AUTOMATION_ENV=config/config_sit.ini && echo. && echo [OK] Entorno activo - Variables configuradas && echo Podes ejecutar: pytest"


