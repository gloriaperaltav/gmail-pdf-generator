#!/usr/bin/env python3
"""
Script para generar un PDF profesional a partir de correos de Gmail.
Usa WeasyPrint para renderizar HTML+CSS.
"""

from datetime import datetime
from weasyprint import HTML, CSS
from io import BytesIO
import html

# Datos de ejemplo - Reemplaza con tus correos reales
CORREOS = [
    {
        "asunto": "[Sentry] KERNEL-BACKEND-WK - TemplateRenderError",
        "remitente": "alerts@sentry.io",
        "destinatario": "tu_email@gmail.com",
        "fecha": "2026-09-25 14:32:00",
        "cuerpo": """Error en la renderización de plantilla en el módulo de backend.

Detalles del error:
- Tipo: TemplateRenderError
- Módulo: kernel-backend
- Línea: 245
- Mensaje: Template variable 'user_name' is undefined

Stack trace:
  File "templates/user_profile.html", line 12
    <h1>Welcome {{ user_name }}</h1>
  File "render.py", line 89, in render_template
    return template.render(context)

Acción recomendada: Verificar que todas las variables de contexto se pasen correctamente al renderizador de plantillas."""
    },
    {
        "asunto": "[Sentry] KERNEL-BACKEND-WJ - ValueError: JSON inválido",
        "remitente": "alerts@sentry.io",
        "destinatario": "tu_email@gmail.com",
        "fecha": "2026-09-25 13:15:00",
        "cuerpo": """Error al parsear JSON en la API de backend.

Detalles del error:
- Tipo: ValueError
- Módulo: kernel-backend
- Endpoint: /api/v1/users/profile
- Mensaje: Expecting value: line 1 column 1 (char 0)

Contexto:
- Método: POST
- Content-Type: application/json
- Payload recibido: (vacío)

Acción recomendada: Validar que el cliente envíe un JSON válido en el body de la solicitud."""
    },
    {
        "asunto": "[Sentry] KERNEL-BACKEND-WH - TimeoutError",
        "remitente": "alerts@sentry.io",
        "destinatario": "tu_email@gmail.com",
        "fecha": "2026-09-25 12:45:00",
        "cuerpo": """Timeout en la conexión a la base de datos.

Detalles del error:
- Tipo: TimeoutError
- Módulo: kernel-backend
- Servicio: PostgreSQL
- Timeout configurado: 30 segundos
- Tiempo transcurrido: 30.5 segundos

Consulta que causó el timeout:
SELECT * FROM users WHERE status='active' AND created_at > NOW() - INTERVAL '30 days'

Acción recomendada: Optimizar la consulta, agregar índices o aumentar el timeout."""
    },
    {
        "asunto": "[Sentry] KERNEL-BACKEND-WG - RuntimeError: Error interno",
        "remitente": "alerts@sentry.io",
        "destinatario": "tu_email@gmail.com",
        "fecha": "2026-09-25 11:20:00",
        "cuerpo": """Error interno no manejado en el procesamiento de solicitud.

Detalles del error:
- Tipo: RuntimeError
- Módulo: kernel-backend
- Función: process_payment
- Mensaje: Error interno del servidor

Información adicional:
- ID de transacción: TXN-2026-09-25-001
- Usuario afectado: user_id_12345
- Servicio externo: Payment Gateway API

Acción recomendada: Revisar los logs del servidor y contactar al proveedor del Payment Gateway."""
    },
    {
        "asunto": "[Sentry] KERNEL-BACKEND-WF - RuntimeError: HTTP 400",
        "remitente": "alerts@sentry.io",
        "destinatario": "tu_email@gmail.com",
        "fecha": "2026-09-25 10:05:00",
        "cuerpo": """Error HTTP 400 en la respuesta de un servicio externo.

Detalles del error:
- Tipo: RuntimeError
- Módulo: kernel-backend
- Servicio externo: Email Service API
- Código HTTP: 400 Bad Request
- Mensaje: Invalid email format in recipient list

Solicitud que falló:
POST https://api.emailservice.com/v2/send
Headers: Authorization: Bearer token_xxx
Body: {"to": ["invalid-email"], "subject": "Test", "body": "Test message"}

Acción recomendada: Validar el formato de emails antes de enviar a servicios externos."""
    }
]

def generar_html_pdf(correos, fecha_reporte):
    """
    Genera el HTML para el PDF con portada, índice y contenido de correos.
    """
    
    # Portada
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Correos Gmail</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            
            .portada {{
                page-break-after: always;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 40px;
            }}
            
            .portada h1 {{
                font-size: 48px;
                margin-bottom: 20px;
                font-weight: 700;
            }}
            
            .portada .fecha {{
                font-size: 24px;
                margin-top: 40px;
                opacity: 0.9;
            }}
            
            .portada .decoracion {{
                margin-top: 60px;
                font-size: 48px;
                opacity: 0.5;
            }}
            
            .indice {{
                page-break-after: always;
                padding: 60px 40px;
            }}
            
            .indice h2 {{
                font-size: 32px;
                color: #667eea;
                margin-bottom: 40px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 15px;
            }}
            
            .indice ol {{
                list-style-position: inside;
                font-size: 16px;
            }}
            
            .indice li {{
                margin-bottom: 15px;
                line-height: 1.8;
                color: #555;
            }}
            
            .correo {{
                page-break-after: always;
                padding: 60px 40px;
                border-top: 4px solid #667eea;
            }}
            
            .correo:first-of-type {{
                border-top: none;
            }}
            
            .correo h2 {{
                font-size: 24px;
                color: #667eea;
                margin-bottom: 30px;
                word-wrap: break-word;
            }}
            
            .correo-meta {{
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border-left: 4px solid #764ba2;
            }}
            
            .correo-meta-item {{
                margin-bottom: 12px;
                display: flex;
                flex-wrap: wrap;
            }}
            
            .correo-meta-label {{
                font-weight: 700;
                color: #667eea;
                min-width: 120px;
                margin-right: 10px;
            }}
            
            .correo-meta-valor {{
                color: #555;
                word-break: break-all;
            }}
            
            .correo-cuerpo {{
                background-color: #fafafa;
                padding: 25px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                font-size: 14px;
                line-height: 1.8;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            
            .pie-pagina {{
                text-align: center;
                font-size: 12px;
                color: #999;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
            
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-center {{
                    content: "Página " counter(page) " de " counter(pages);
                    font-size: 12px;
                    color: #999;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- PORTADA -->
        <div class="portada">
            <h1>📧 Reporte de Correos Gmail</h1>
            <div class="fecha">{fecha_reporte}</div>
            <div class="decoracion">✉️</div>
        </div>
        
        <!-- ÍNDICE -->
        <div class="indice">
            <h2>Índice de Correos</h2>
            <ol>
    """
    
    # Agregar items al índice
    for i, correo in enumerate(correos, 1):
        html_content += f'<li>{correo["asunto"]}</li>\n'
    
    html_content += """
            </ol>
        </div>
    """
    
    # Agregar páginas de correos
    for correo in correos:
        html_content += f"""
        <div class="correo">
            <h2>{html.escape(correo['asunto'])}</h2>
            
            <div class="correo-meta">
                <div class="correo-meta-item">
                    <span class="correo-meta-label">Remitente:</span>
                    <span class="correo-meta-valor">{html.escape(correo['remitente'])}</span>
                </div>
                <div class="correo-meta-item">
                    <span class="correo-meta-label">Destinatario:</span>
                    <span class="correo-meta-valor">{html.escape(correo['destinatario'])}</span>
                </div>
                <div class="correo-meta-item">
                    <span class="correo-meta-label">Fecha:</span>
                    <span class="correo-meta-valor">{html.escape(correo['fecha'])}</span>
                </div>
            </div>
            
            <div class="correo-cuerpo">
{html.escape(correo['cuerpo'])}
            </div>
            
            <div class="pie-pagina">
                Generado automáticamente • Reporte de Correos Gmail
            </div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    return html_content

def generar_pdf(nombre_archivo="correos_gmail.pdf"):
    """
    Genera el PDF a partir de los correos.
    """
    try:
        # Obtener fecha actual formateada
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
        
        # Generar HTML
        html_content = generar_html_pdf(CORREOS, fecha_reporte)
        
        # Convertir HTML a PDF
        HTML(string=html_content).write_pdf(nombre_archivo)
        
        print(f"✅ PDF generado exitosamente: {nombre_archivo}")
        print(f"📊 Estadísticas:")
        print(f"   - Correos incluidos: {len(CORREOS)}")
        print(f"   - Fecha del reporte: {fecha_reporte}")
        print(f"   - Tamaño del archivo: {__import__('os').path.getsize(nombre_archivo) / 1024:.2f} KB")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error: Falta instalar una dependencia.")
        print(f"   Ejecuta: pip install weasyprint")
        print(f"   Detalles: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando generación de PDF de correos...")
    print()
    
    exito = generar_pdf()
    
    if exito:
        print()
        print("✨ Proceso completado exitosamente.")
        print("📁 El archivo 'correos_gmail.pdf' está listo para usar.")
    else:
        print()
        print("⚠️  Hubo un problema durante la generación.")
