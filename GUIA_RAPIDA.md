# 🚀 Guía Rápida - Gmail PDF Generator

## ⚡ Inicio en 5 minutos

### Paso 1: Descargar el proyecto

```bash
git clone https://github.com/gloriaperaltav/gmail-pdf-generator.git
cd gmail-pdf-generator
```

### Paso 2: Instalar dependencias

**En Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**En Windows:**
```bash
setup.bat
```

**Manual (cualquier SO):**
```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar

**Opción A - Modo Demo (sin Gmail):**
```bash
python generar_pdf_correos.py
```

**Opción B - Modo Real (con Gmail):**
```bash
python generar_pdf_desde_gmail.py
```

## 📋 Requisitos Previos

- ✅ Python 3.7+
- ✅ pip
- ✅ Conexión a internet (solo para modo Gmail)

## 🎯 Casos de Uso

### Caso 1: Generar PDF de ejemplo rápidamente

```bash
python generar_pdf_correos.py
```

**Resultado:** `correos_gmail.pdf` con 5 correos de ejemplo

### Caso 2: Generar PDF desde tus correos reales

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear proyecto → Habilitar Gmail API → Descargar credenciales
3. Guardar como `credentials.json` en la carpeta del proyecto
4. Ejecutar:
   ```bash
   python generar_pdf_desde_gmail.py
   ```

### Caso 3: Personalizar los correos

Editar `generar_pdf_correos.py` y modificar la lista `CORREOS`:

```python
CORREOS = [
    {
        "asunto": "Mi asunto",
        "remitente": "de@example.com",
        "destinatario": "para@example.com",
        "fecha": "2026-09-25 10:00:00",
        "cuerpo": "Contenido del mensaje..."
    }
]
```

### Caso 4: Ver ejemplos avanzados

```bash
python ejemplo_avanzado.py
```

## 🎨 Personalizar Estilos

Los estilos CSS están en las funciones `generar_html_pdf()`:

```python
# Cambiar colores
#667eea → tu color primario
#764ba2 → tu color secundario

# Cambiar márgenes
@page { margin: 2cm; }

# Cambiar fuentes
font-family: 'Tu fuente aquí'
```

## 📊 Estructura del PDF Generado

```
1. Portada
   - Título: "Reporte de Correos Gmail"
   - Fecha actual
   - Diseño con gradiente

2. Índice
   - Lista de todos los correos por asunto

3. Páginas de Correos
   - Una página por correo
   - Metadatos (remitente, destinatario, fecha)
   - Cuerpo del mensaje
   - Numeración automática
```

## 🔧 Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: weasyprint` | `pip install weasyprint` |
| `ModuleNotFoundError: google` | `pip install google-auth-oauthlib` |
| `credentials.json not found` | Descargar desde Google Cloud Console |
| WeasyPrint no funciona en Windows | Instalar GTK+ desde [aquí](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) |
| PDF vacío | Verificar que los correos existan en Gmail |

## 📁 Archivos Principales

```
gmail-pdf-generator/
├── generar_pdf_correos.py          # Script principal (modo demo)
├── generar_pdf_desde_gmail.py      # Script con Gmail API
├── ejemplo_avanzado.py             # Ejemplos de uso
├── requirements.txt                # Dependencias
├── setup.sh                        # Instalación Linux/macOS
├── setup.bat                       # Instalación Windows
├── README.md                       # Documentación completa
└── GUIA_RAPIDA.md                 # Esta guía
```

## 💡 Tips Útiles

### Filtrar correos de Gmail

```python
# Solo de Sentry
generar_pdf_desde_gmail(query="from:alerts@sentry.io")

# Con palabra clave
generar_pdf_desde_gmail(query="subject:ERROR")

# No leídos
generar_pdf_desde_gmail(query="is:unread")

# Últimos 7 días
generar_pdf_desde_gmail(query="newer_than:7d")
```

### Cambiar nombre del PDF

```python
generar_pdf("mi_reporte.pdf")
```

### Aumentar cantidad de correos

```python
generar_pdf_desde_gmail(cantidad=10)
```

## 🔐 Seguridad

- ✅ Las credenciales se guardan localmente en `token.pickle`
- ✅ Solo lectura de correos (permisos `gmail.readonly`)
- ✅ No se envían datos a servidores externos
- ✅ Puedes revocar acceso desde tu cuenta de Google

## 📞 Ayuda

- 📖 Lee el [README.md](README.md) completo
- 🐛 Abre un issue en GitHub
- 💬 Revisa los ejemplos en `ejemplo_avanzado.py`

## 🎓 Próximos Pasos

1. ✅ Ejecuta el script de demo
2. ✅ Personaliza los estilos CSS
3. ✅ Configura Gmail API para correos reales
4. ✅ Automatiza con cron/Task Scheduler

---

**¡Listo! Ya puedes generar PDFs profesionales desde tus correos. 🎉**
