@echo off
echo === Activando entorno virtual y configurando variables ===

if not exist crowdar_env\Scripts\activate.bat (
    echo ERROR: No se encontro el entorno virtual 'crowdar_env'.
    echo Ejecuta primero: configure_tool.bat
    pause
    exit /b 1
)

cmd /k ".\crowdar_env\Scripts\activate.bat && set BIZ_AUTOMATION_ENV=config/config_sit.ini && echo. && echo [OK] Entorno activo - Variables configuradas && echo Podes ejecutar: pytest"

