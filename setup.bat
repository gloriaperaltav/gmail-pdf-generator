@echo off
REM Script de instalación para Gmail PDF Generator en Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     Gmail PDF Generator - Script de Instalación (Windows) ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado.
    echo    Por favor, instala Python 3.7 o superior desde:
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version
echo.

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 📥 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✨ Instalación completada                    ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo 📝 Próximos pasos:
echo.
echo 1. Activar el entorno virtual:
echo    venv\Scripts\activate.bat
echo.
echo 2. Ejecutar el script de ejemplo:
echo    python generar_pdf_correos.py
echo.
echo 3. Para usar Gmail real, configura las credenciales:
echo    - Ve a: https://console.cloud.google.com/
echo    - Descarga credentials.json
echo    - Ejecuta: python generar_pdf_desde_gmail.py
echo.
echo 4. Ver ejemplos avanzados:
echo    python ejemplo_avanzado.py
echo.

pause
