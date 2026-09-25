#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que todo funciona correctamente.
"""

import sys
import os
from datetime import datetime

def verificar_python():
    """Verifica la versión de Python."""
    print("🔍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Se requiere 3.7+")
        return False

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas."""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = {
        'weasyprint': 'WeasyPrint',
        'google.auth': 'Google Auth',
        'google.oauth2': 'Google OAuth2',
        'googleapiclient': 'Google API Client'
    }
    
    todas_ok = True
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"   ✅ {nombre} - OK")
        except ImportError:
            print(f"   ❌ {nombre} - NO INSTALADO")
            todas_ok = False
    
    return todas_ok

def verificar_archivos():
    """Verifica que los archivos principales existan."""
    print("\n🔍 Verificando archivos...")
    
    archivos = [
        'generar_pdf_correos.py',
        'generar_pdf_desde_gmail.py',
        'ejemplo_avanzado.py',
        'requirements.txt',
        'README.md',
        'GUIA_RAPIDA.md'
    ]
    
    todas_ok = True
    for archivo in archivos:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo)
            print(f"   ✅ {archivo} ({tamaño} bytes)")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            todas_ok = False
    
    return todas_ok

def probar_generacion_pdf():
    """Intenta generar un PDF de prueba."""
    print("\n🔍 Probando generación de PDF...")
    
    try:
        from generar_pdf_correos import generar_pdf
        
        # Generar PDF de prueba
        print("   📄 Generando PDF de prueba...")
        exito = generar_pdf("test_output.pdf")
        
        if exito and os.path.exists("test_output.pdf"):
            tamaño = os.path.getsize("test_output.pdf") / 1024
            print(f"   ✅ PDF generado exitosamente ({tamaño:.2f} KB)")
            
            # Limpiar archivo de prueba
            os.remove("test_output.pdf")
            print("   🧹 Archivo de prueba eliminado")
            return True
        else:
            print("   ❌ Error al generar PDF")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def mostrar_resumen(resultados):
    """Muestra un resumen de los resultados."""
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    total = len(resultados)
    exitosas = sum(resultados.values())
    fallidas = total - exitosas
    
    print(f"\n✅ Pruebas exitosas: {exitosas}/{total}")
    print(f"❌ Pruebas fallidas: {fallidas}/{total}")
    
    if fallidas == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecutar: python generar_pdf_correos.py")
        print("   2. Revisar el PDF generado: correos_gmail.pdf")
        print("   3. Para usar Gmail real, seguir la guía en README.md")
        return True
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        print("\n📝 Soluciones:")
        if not resultados.get('dependencias', False):
            print("   - Instalar dependencias: pip install -r requirements.txt")
        if not resultados.get('archivos', False):
            print("   - Verificar que estés en la carpeta correcta")
        if not resultados.get('pdf', False):
            print("   - Revisar los logs de error arriba")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA RÁPIDA - Gmail PDF Generator")
    print("=" * 60)
    print(f"\n📅 Fecha: {datetime.now().strftime('%d de %B de %Y %H:%M:%S')}")
    print()
    
    resultados = {
        'python': verificar_python(),
        'dependencias': verificar_dependencias(),
        'archivos': verificar_archivos(),
        'pdf': probar_generacion_pdf()
    }
    
    exito = mostrar_resumen(resultados)
    
    print("\n" + "=" * 60)
    
    return 0 if exito else 1

if __name__ == "__main__":
    sys.exit(main())
