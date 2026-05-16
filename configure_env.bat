@echo off
echo "configurando variables de entorno"
cmd /k ".\crowdar_env\Scripts\activate.bat && set BIZ_AUTOMATION_ENV=config/config_sit.ini && echo Variables de entorno configuradas OK"

