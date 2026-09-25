# 📧 Generador de PDF desde Correos Gmail

Script Python efímero que genera un PDF profesional a partir de correos de Gmail con portada, índice y páginas formateadas.

## ✨ Características

- ✅ **Portada profesional** con gradiente y fecha
- ✅ **Índice automático** con listado de correos
- ✅ **Páginas formateadas** con metadatos y cuerpo del mensaje
- ✅ **Diseño responsivo** con CSS moderno
- ✅ **Saltos de página** automáticos entre correos
- ✅ **Márgenes y tipografía** profesionales
- ✅ **Numeración de páginas** automática
- ✅ **Dos modos de operación**:
  - Modo demo con datos de ejemplo
  - Modo real con integración a Gmail API

## 📋 Requisitos

- Python 3.7+
- pip (gestor de paquetes)

## 🚀 Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/gloriaperaltav/gmail-pdf-generator.git
cd gmail-pdf-generator
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota:** WeasyPrint requiere dependencias del sistema. Si tienes problemas:

**En Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
```

**En macOS:**
```bash
brew install python3 libffi openssl
```

**En Windows:**
Descarga e instala GTK+ desde: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

## 💻 Uso

### Opción 1: Modo Demo (Datos de Ejemplo)

Genera un PDF con 5 correos de ejemplo sin necesidad de autenticación:

```bash
python generar_pdf_correos.py
```

**Salida esperada:**
```
🚀 Iniciando generación de PDF de correos...

✅ PDF generado exitosamente: correos_gmail.pdf
📊 Estadísticas:
   - Correos incluidos: 5
   - Fecha del reporte: 25 de Septiembre de 2026
   - Tamaño del archivo: 245.32 KB

✨ Proceso completado exitosamente.
📁 El archivo 'correos_gmail.pdf' está listo para usar.
```

### Opción 2: Modo Real (Desde Gmail)

Obtiene correos reales de tu cuenta de Gmail:

#### Paso 1: Configurar Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita la **Gmail API**
4. Crea credenciales OAuth 2.0 (tipo: Aplicación de escritorio)
5. Descarga el archivo JSON y guárdalo como `credentials.json` en la carpeta del proyecto

#### Paso 2: Ejecutar el script

```bash
python generar_pdf_desde_gmail.py
```

**Primera ejecución:**
- Se abrirá una ventana del navegador para autenticarte
- Autoriza el acceso a tu Gmail
- Las credenciales se guardarán en `token.pickle` para futuras ejecuciones

**Salida esperada:**
```
🚀 Generador de PDF desde Gmail
==================================================

📧 Obteniendo correos de Gmail...
✅ Se obtuvieron 5 correos

🎨 Generando HTML...
📄 Renderizando PDF...
✅ PDF generado exitosamente: correos_gmail.pdf
📊 Estadísticas:
   - Correos incluidos: 5
   - Fecha del reporte: 25 de Septiembre de 2026
   - Tamaño del archivo: 312.45 KB

✨ Proceso completado exitosamente.
```

## 📝 Personalización

### Modificar los correos de ejemplo

Edita la lista `CORREOS` en `generar_pdf_correos.py`:

```python
CORREOS = [
    {
        "asunto": "Tu asunto aquí",
        "remitente": "remitente@example.com",
        "destinatario": "tu_email@gmail.com",
        "fecha": "2026-09-25 14:32:00",
        "cuerpo": "Contenido del mensaje..."
    },
    # ... más correos
]
```

### Cambiar el filtro de Gmail

En `generar_pdf_desde_gmail.py`, modifica el parámetro `query`:

```python
# Obtener correos de Sentry
generar_pdf_desde_gmail(cantidad=5, query="from:alerts@sentry.io")

# Obtener correos con palabra clave
generar_pdf_desde_gmail(cantidad=5, query="subject:ERROR")

# Obtener correos no leídos
generar_pdf_desde_gmail(cantidad=5, query="is:unread")
```

### Personalizar estilos CSS

Los estilos están en la sección `<style>` dentro de las funciones `generar_html_pdf()`. Puedes modificar:

- **Colores:** Cambia `#667eea` y `#764ba2` por tus colores preferidos
- **Fuentes:** Modifica `font-family`
- **Márgenes:** Ajusta los valores en `@page { margin: 2cm; }`
- **Tamaños:** Cambia `font-size` en cada clase

## 📊 Estructura del PDF

```
┌─────────────────────────────────┐
│         PORTADA                 │
│  Reporte de Correos Gmail       │
│  25 de Septiembre de 2026       │
└─────────────────────────────────┘
         [Salto de página]
┌─────────────────────────────────┐
│         ÍNDICE                  │
│  1. [Sentry] KERNEL-BACKEND-WK  │
│  2. [Sentry] KERNEL-BACKEND-WJ  │
│  3. [Sentry] KERNEL-BACKEND-WH  │
│  4. [Sentry] KERNEL-BACKEND-WG  │
│  5. [Sentry] KERNEL-BACKEND-WF  │
└─────────────────────────────────┘
         [Salto de página]
┌─────────────────────────────────┐
│  [Sentry] KERNEL-BACKEND-WK     │
│  Remitente: alerts@sentry.io    │
│  Destinatario: tu_email@...     │
│  Fecha: 2026-09-25 14:32:00     │
│                                 │
│  [Cuerpo del mensaje]           │
└─────────────────────────────────┘
         [Salto de página]
│  ... más correos ...            │
```

## 🔒 Seguridad

- Las credenciales de Gmail se guardan localmente en `token.pickle`
- El script solo tiene permisos de lectura (`gmail.readonly`)
- No se envían datos a servidores externos
- Puedes revocar el acceso en cualquier momento desde tu cuenta de Google

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'weasyprint'"

```bash
pip install weasyprint
```

### Error: "No module named 'google'"

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Error: "credentials.json not found"

Asegúrate de haber descargado el archivo de credenciales desde Google Cloud Console y guardarlo en la carpeta del proyecto.

### El PDF se genera pero está vacío

- Verifica que los correos existan en tu Gmail
- Prueba con un filtro más general: `query=""`
- Aumenta la cantidad: `cantidad=10`

### WeasyPrint no funciona en Windows

Descarga e instala GTK+ desde:
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

## 📄 Licencia

MIT License - Libre para usar y modificar

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o sugerencias, abre un issue en el repositorio.

---

**Hecho con ❤️ para automatizar la generación de reportes de correos**
