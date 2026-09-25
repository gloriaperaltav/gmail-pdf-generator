#!/bin/bash

# Script de instalación rápida para Gmail PDF Generator
# Compatible con Linux y macOS

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     Gmail PDF Generator - Script de Instalación           ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado."
    echo "   Por favor, instala Python 3.7 o superior."
    exit 1
fi

echo "✅ Python 3 detectado: $(python3 --version)"
echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "📥 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║              ✨ Instalación completada                    ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📝 Próximos pasos:"
echo ""
echo "1. Activar el entorno virtual:"
echo "   source venv/bin/activate"
echo ""
echo "2. Ejecutar el script de ejemplo:"
echo "   python generar_pdf_correos.py"
echo ""
echo "3. Para usar Gmail real, configura las credenciales:"
echo "   - Ve a: https://console.cloud.google.com/"
echo "   - Descarga credentials.json"
echo "   - Ejecuta: python generar_pdf_desde_gmail.py"
echo ""
echo "4. Ver ejemplos avanzados:"
echo "   python ejemplo_avanzado.py"
echo ""
