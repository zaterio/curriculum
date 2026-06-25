# CV Hacker - Daniel Ortiz

Generador de currículum vitae con estilo **hacker/terminal** a partir de un archivo de texto plano.

El objetivo es separar completamente el **contenido** del **diseño**: tú editas un archivo `.txt` simple, y el script se encarga de generar el HTML y el PDF con el estilo visual.

---

## ¿Qué hace este proyecto?

- Toma el contenido de `cv_ortiz_datos.txt`.
- Genera `cv_ortiz_hacker.html` con estilo de terminal oscura, texto verde neón, fuente monoespaciada y efectos de hacker.
- Genera `cv_ortiz_hacker.pdf` usando Google Chrome en modo headless.
- Permite usar variables como `@nombre`, `@email`, `@experiencia` dentro del texto para no repetir datos.

---

## Archivos del proyecto

| Archivo | Descripción |
|---------|-------------|
| `cv_ortiz_datos.txt` | **Archivo principal de contenido.** Edita este archivo para actualizar tu CV. |
| `generar_cv.py` | Script Python que lee el `.txt` y genera el HTML y el PDF. |
| `cv_ortiz_hacker.html` | CV generado con estilo hacker. **Se sobrescribe** al ejecutar el script. |
| `cv_ortiz_hacker.pdf` | CV final listo para enviar. **Se sobrescribe** al ejecutar el script. |
| `README.md` | Esta documentación. |

---

## Requisitos

- **Python 3** (cualquier versión reciente)
- **Google Chrome** instalado (se usa en modo headless para generar el PDF)

No se requieren librerías externas de Python. El script usa solo la librería estándar.

---

## Uso rápido

```bash
cd /home/zaterio/dev/curriculum-cv
python3 generar_cv.py
```

Eso genera:

- `cv_ortiz_hacker.html`
- `cv_ortiz_hacker.pdf`

Para subir cambios a GitHub:

```bash
git add .
git commit -m "update: descripción del cambio"
git push
```

---

## Formato de `cv_ortiz_datos.txt`

### 1. Metadatos (encabezado)

Al inicio del archivo, líneas que empiezan con `@`:

```text
@nombre Daniel Ortiz
@titulo Senior DevOps | SysAdmin | Backend | CyberSec
@email daniel.ortiz@zka.cl
@experiencia +15 años de experiencia
@ubicacion Chile
```

Estos valores se usan en el encabezado del CV y pueden reutilizarse dentro del contenido escribiendo `@nombre`, `@email`, etc.

### 2. Secciones

Cada sección empieza con `[Nombre de la Sección]`:

```text
[Perfil Ejecutivo]
Texto del perfil. Puedes usar @experiencia para insertar automáticamente
"+15 años de experiencia".

[DevOps / SysAdmin]
- Item uno
- Item dos
- Item tres
```

### 3. Proyectos

Dentro de una sección, los proyectos se definen así:

```text
# Nombre del Proyecto
> Año // Cliente // Detalle adicional
Descripción del proyecto en una o varias líneas.
```

Ejemplo:

```text
# Claro Box Monit
> 2024-2025 // Claro
Sistema Django + Celery + RabbitMQ + Ansible para monitoreo y gestión
remota de rigs/equipos de campo.
```

### 4. Habilidades técnicas

La sección `[Habilidades Técnicas Senior]` es especial: cada palabra se convierte en una etiqueta tipo "skill tag":

```text
[Habilidades Técnicas Senior]
Python Go Bash Django FastAPI PostgreSQL MongoDB Redis Docker Kubernetes
Ansible Terraform Proxmox Ceph Suricata Snort
```

### 5. Texto adicional en gris

Líneas que empiezan con `+` se muestran en color verde tenue (clase `.dim`):

```text
+ Conocimientos adicionales: análisis de datos, liderazgo técnico, mentoría.
```

### 6. Referencias

Las referencias también se definen como proyectos:

```text
[Referencias]
# Nombre Completo
> Cargo, Empresa
email@ejemplo.com | +56 9 1234 5678
```

---

## Ejemplo completo de sección

```text
[Proyectos Recientes (últimos 2 años)]

# 4K-IA Transcoder
> 2024-2025 // Pipeline propio
Pipeline de transcodificación y mejora de video en vivo con IA: denoising
DnCNN, super-resolución ESPCN y Real-ESRGAN, orquestado con FFmpeg +
ONNX Runtime GPU + Ansible.

# Claro Box Monit
> 2024-2025 // Claro
Sistema Django + Celery + RabbitMQ + Ansible para monitoreo y gestión
remota de rigs/equipos de campo.
```

---

## Reglas importantes

- Deja una **línea en blanco** entre proyectos para separarlos correctamente.
- Las líneas que empiezan con `#` dentro de una sección siempre se interpretan como título de proyecto.
- Las líneas que empiezan con `>` se interpretan como metadata del proyecto inmediatamente anterior.
- Las líneas que empiezan con `-` se interpretan como items de lista.
- Puedes usar `@clave` dentro del texto y se reemplazará por el valor del metadato correspondiente.

---

## Personalizar el diseño

Si quieres cambiar colores, fuentes, layout o efectos visuales, edita la variable `HTML_TEMPLATE` dentro de `generar_cv.py`. El CSS está embebido en esa plantilla.

No edites `cv_ortiz_hacker.html` manualmente, porque se sobrescribe cada vez que ejecutas el generador.

---

## Estructura del script `generar_cv.py`

| Función | Propósito |
|---------|-----------|
| `parse_cv_data()` | Lee y parsea `cv_ortiz_datos.txt` en una estructura de datos. |
| `replace_meta_tokens()` | Reemplaza `@clave` por el valor de los metadatos. |
| `render_html()` | Genera el HTML final inyectando el contenido en la plantilla. |
| `render_seccion()` | Renderiza cada sección según su tipo. |
| `render_proyecto()` | Renderiza un proyecto con título, metadata y descripción. |
| `generate_pdf()` | Llama a Google Chrome headless para crear el PDF. |

---

## Solución de problemas

### Error: `google-chrome` no encontrado

Asegúrate de tener Google Chrome instalado y disponible en el PATH:

```bash
which google-chrome
```

Si usas Chromium, edita la función `generate_pdf()` en `generar_cv.py` y cambia `"google-chrome"` por `"chromium-browser"` o `"chromium"`.

### El PDF se ve cortado o con páginas en blanco

Ajusta los márgenes o el tamaño de fuente en la plantilla CSS dentro de `generar_cv.py`.

### Los proyectos no se separan bien

Revisa que haya una línea en blanco entre cada proyecto en `cv_ortiz_datos.txt`.

---

## Autor

**Daniel Ortiz** — daniel.ortiz@zka.cl

---

## Licencia

Uso personal. Puedes adaptar el generador para tu propio CV si lo deseas.
