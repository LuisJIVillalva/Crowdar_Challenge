@echo off
echo "Instalando virtualEnv"
pip install virtualenv
echo "Creando ambiente virtualEnv"
virtualenv -p "C:\Python314\python.exe" crowdar_env
echo "Iniciando ambiente virtual"
call .\.venv\Scripts\activate.bat
echo "Upgrade pip"
python -m pip install --upgrade pip
echo "Instalando librerias"
pip install -r requirements.txt
echo "configurando variables de entorno"
echo ""
echo "=== Setup completo. Activando entorno virtual... ==="
cmd /k ".\crowdar_env\Scripts\activate.bat && set BIZ_AUTOMATION_ENV=configs/config_sit.ini && echo Variables de entorno configuradas OK"

