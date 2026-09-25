#!/usr/bin/env python3
"""
Ejemplo avanzado: Generador de PDF con opciones personalizadas.
Demuestra cómo usar el script con diferentes configuraciones.
"""

from generar_pdf_correos import generar_pdf, CORREOS
from datetime import datetime
import os

def ejemplo_1_pdf_basico():
    """Genera un PDF básico con los datos de ejemplo."""
    print("=" * 60)
    print("EJEMPLO 1: PDF Básico")
    print("=" * 60)
    print()
    
    generar_pdf("ejemplo_1_basico.pdf")
    print()

def ejemplo_2_pdf_personalizado():
    """Genera un PDF con correos personalizados."""
    print("=" * 60)
    print("EJEMPLO 2: PDF Personalizado")
    print("=" * 60)
    print()
    
    # Importar la función para generar HTML
    from generar_pdf_correos import generar_html_pdf
    from weasyprint import HTML
    
    # Crear correos personalizados
    correos_personalizados = [
        {
            "asunto": "Reunión de equipo - Lunes 10:00 AM",
            "remitente": "manager@empresa.com",
            "destinatario": "tu_email@empresa.com",
            "fecha": "2026-09-25 09:30:00",
            "cuerpo": """Hola,

Te confirmo la reunión de equipo para el próximo lunes a las 10:00 AM en la sala de conferencias.

Agenda:
1. Revisión de proyectos en curso
2. Discusión de nuevas iniciativas
3. Asignación de tareas

Por favor, trae tus notas y cualquier actualización de tu área.

Saludos,
Manager"""
        },
        {
            "asunto": "Aprobación de presupuesto Q4",
            "remitente": "finance@empresa.com",
            "destinatario": "tu_email@empresa.com",
            "fecha": "2026-09-24 16:45:00",
            "cuerpo": """Estimado,

Tu solicitud de presupuesto para Q4 ha sido aprobada.

Detalles:
- Monto aprobado: $50,000
- Período: Octubre - Diciembre 2026
- Referencia: BUD-2026-Q4-001

Por favor, utiliza esta referencia en todos los gastos relacionados.

Finanzas"""
        }
    ]
    
    # Generar HTML con correos personalizados
    fecha_reporte = datetime.now().strftime("%d de %B de %Y").replace(
        "January", "Enero"
    ).replace(
        "February", "Febrero"
    ).replace(
        "March", "Marzo"
    ).replace(
        "April", "Abril"
    ).replace(
        "May", "Mayo"
    ).replace(
        "June", "Junio"
    ).replace(
        "July", "Julio"
    ).replace(
        "August", "Agosto"
    ).replace(
        "September", "Septiembre"
    ).replace(
        "October", "Octubre"
    ).replace(
        "November", "Noviembre"
    ).replace(
        "December", "Diciembre"
    )
    
    html_content = generar_html_pdf(correos_personalizados, fecha_reporte)
    HTML(string=html_content).write_pdf("ejemplo_2_personalizado.pdf")
    
    print("✅ PDF generado: ejemplo_2_personalizado.pdf")
    print(f"📊 Correos incluidos: {len(correos_personalizados)}")
    print()

def ejemplo_3_filtrar_correos():
    """Demuestra cómo filtrar correos por criterios."""
    print("=" * 60)
    print("EJEMPLO 3: Filtrado de Correos")
    print("=" * 60)
    print()
    
    # Filtrar solo correos de Sentry
    correos_sentry = [c for c in CORREOS if "[Sentry]" in c["asunto"]]
    print(f"✅ Correos de Sentry encontrados: {len(correos_sentry)}")
    for correo in correos_sentry:
        print(f"   - {correo['asunto']}")
    print()

def ejemplo_4_estadisticas():
    """Muestra estadísticas de los correos."""
    print("=" * 60)
    print("EJEMPLO 4: Estadísticas de Correos")
    print("=" * 60)
    print()
    
    print(f"Total de correos: {len(CORREOS)}")
    print()
    
    print("Remitentes:")
    remitentes = set(c["remitente"] for c in CORREOS)
    for remitente in remitentes:
        cantidad = sum(1 for c in CORREOS if c["remitente"] == remitente)
        print(f"   - {remitente}: {cantidad} correo(s)")
    print()
    
    print("Palabras clave en asuntos:")
    palabras_clave = {}
    for correo in CORREOS:
        palabras = correo["asunto"].split()
        for palabra in palabras:
            if len(palabra) > 3:  # Solo palabras de más de 3 caracteres
                palabras_clave[palabra] = palabras_clave.get(palabra, 0) + 1
    
    for palabra, cantidad in sorted(palabras_clave.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   - {palabra}: {cantidad} veces")
    print()

def ejemplo_5_listar_archivos():
    """Lista los archivos PDF generados."""
    print("=" * 60)
    print("EJEMPLO 5: Archivos Generados")
    print("=" * 60)
    print()
    
    pdfs = [f for f in os.listdir(".") if f.endswith(".pdf")]
    
    if pdfs:
        print(f"Se encontraron {len(pdfs)} archivo(s) PDF:")
        for pdf in pdfs:
            tamaño = os.path.getsize(pdf) / 1024
            print(f"   - {pdf} ({tamaño:.2f} KB)")
    else:
        print("No se encontraron archivos PDF.")
    print()

def main():
    """Ejecuta todos los ejemplos."""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  EJEMPLOS DE USO - Generador de PDF desde Gmail".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Ejecutar ejemplos
    ejemplo_1_pdf_basico()
    ejemplo_2_pdf_personalizado()
    ejemplo_3_filtrar_correos()
    ejemplo_4_estadisticas()
    ejemplo_5_listar_archivos()
    
    print("=" * 60)
    print("✨ Todos los ejemplos completados")
    print("=" * 60)

if __name__ == "__main__":
    main()
