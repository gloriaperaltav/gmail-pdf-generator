#!/usr/bin/env python3
"""
Script para obtener correos reales de Gmail y generar un PDF profesional.
Requiere autenticación con Google OAuth2.
"""

import os
import pickle
import base64
from datetime import datetime
from weasyprint import HTML
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core import retry
from googleapiclient.discovery import build
import html as html_module

# Scopes de Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def autenticar_gmail():
    """
    Autentica con Gmail API usando OAuth2.
    Guarda las credenciales en token.pickle para reutilizarlas.
    """
    creds = None
    
    # Cargar credenciales guardadas
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Si no hay credenciales válidas, obtener nuevas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guardar credenciales para próximas ejecuciones
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def obtener_correos_gmail(cantidad=5, query=""):
    """
    Obtiene correos de Gmail.
    
    Args:
        cantidad: Número de correos a obtener
        query: Filtro de búsqueda (ej: "from:alerts@sentry.io")
    """
    try:
        creds = autenticar_gmail()
        service = build('gmail', 'v1', credentials=creds)
        
        # Buscar correos
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=cantidad
        ).execute()
        
        mensajes = results.get('messages', [])
        
        if not mensajes:
            print("⚠️  No se encontraron correos con los criterios especificados.")
            return []
        
        correos = []
        for msg in mensajes:
            # Obtener detalles del mensaje
            mensaje = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            headers = mensaje['payload']['headers']
            
            # Extraer información
            asunto = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
            remitente = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
            destinatario = next((h['value'] for h in headers if h['name'] == 'To'), 'Desconocido')
            fecha = next((h['value'] for h in headers if h['name'] == 'Date'), 'Desconocida')
            
            # Extraer cuerpo
            cuerpo = ""
            if 'parts' in mensaje['payload']:
                for part in mensaje['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            cuerpo = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
            else:
                data = mensaje['payload']['body'].get('data', '')
                if data:
                    cuerpo = base64.urlsafe_b64decode(data).decode('utf-8')
            
            correos.append({
                'asunto': asunto,
                'remitente': remitente,
                'destinatario': destinatario,
                'fecha': fecha,
                'cuerpo': cuerpo[:1000]  # Limitar a 1000 caracteres
            })
        
        return correos
        
    except FileNotFoundError:
        print("❌ Error: No se encontró 'credentials.json'")
        print("   Descarga tus credenciales de Google Cloud Console:")
        print("   https://console.cloud.google.com/apis/credentials")
        return []
    except Exception as e:
        print(f"❌ Error al conectar con Gmail: {e}")
        return []

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
        html_content += f'<li>{html_module.escape(correo["asunto"])}</li>\n'
    
    html_content += """
            </ol>
        </div>
    """
    
    # Agregar páginas de correos
    for correo in correos:
        html_content += f"""
        <div class="correo">
            <h2>{html_module.escape(correo['asunto'])}</h2>
            
            <div class="correo-meta">
                <div class="correo-meta-item">
                    <span class="correo-meta-label">Remitente:</span>
                    <span class="correo-meta-valor">{html_module.escape(correo['remitente'])}</span>
                </div>
                <div class="correo-meta-item">
                    <span class="correo-meta-label">Destinatario:</span>
                    <span class="correo-meta-valor">{html_module.escape(correo['destinatario'])}</span>
                </div>
                <div class="correo-meta-item">
                    <span class="correo-meta-label">Fecha:</span>
                    <span class="correo-meta-valor">{html_module.escape(correo['fecha'])}</span>
                </div>
            </div>
            
            <div class="correo-cuerpo">
{html_module.escape(correo['cuerpo'])}
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

def generar_pdf_desde_gmail(cantidad=5, query="", nombre_archivo="correos_gmail.pdf"):
    """
    Obtiene correos de Gmail y genera un PDF.
    """
    try:
        print("📧 Obteniendo correos de Gmail...")
        correos = obtener_correos_gmail(cantidad, query)
        
        if not correos:
            print("❌ No se pudieron obtener correos.")
            return False
        
        print(f"✅ Se obtuvieron {len(correos)} correos")
        print()
        
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
        print("🎨 Generando HTML...")
        html_content = generar_html_pdf(correos, fecha_reporte)
        
        # Convertir HTML a PDF
        print("📄 Renderizando PDF...")
        HTML(string=html_content).write_pdf(nombre_archivo)
        
        print(f"✅ PDF generado exitosamente: {nombre_archivo}")
        print(f"📊 Estadísticas:")
        print(f"   - Correos incluidos: {len(correos)}")
        print(f"   - Fecha del reporte: {fecha_reporte}")
        print(f"   - Tamaño del archivo: {os.path.getsize(nombre_archivo) / 1024:.2f} KB")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error: Falta instalar una dependencia.")
        print(f"   Ejecuta: pip install weasyprint google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        print(f"   Detalles: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Generador de PDF desde Gmail")
    print("=" * 50)
    print()
    
    # Ejemplo: obtener últimos 5 correos de Sentry
    exito = generar_pdf_desde_gmail(
        cantidad=5,
        query="from:alerts@sentry.io",
        nombre_archivo="correos_gmail.pdf"
    )
    
    if exito:
        print()
        print("✨ Proceso completado exitosamente.")
    else:
        print()
        print("⚠️  Hubo un problema durante la generación.")
