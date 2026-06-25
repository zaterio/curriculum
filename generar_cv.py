#!/usr/bin/env python3
"""
generar_cv.py

Lee el contenido del CV desde cv_ortiz_datos.txt y genera:
  - cv_ortiz_hacker.html  (versión con estilo hacker/terminal)
  - cv_ortiz_hacker.pdf   (PDF generado con Google Chrome headless)

Uso:
  cd /home/zaterio/dev/curriculum-cv
  python3 generar_cv.py
"""

import os
import re
import subprocess
import sys
from html import escape

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "cv_ortiz_datos.txt")
HTML_FILE = os.path.join(BASE_DIR, "cv_ortiz_hacker.html")
PDF_FILE = os.path.join(BASE_DIR, "cv_ortiz_hacker.pdf")

# ---------------------------------------------------------------------------
# PLANTILLA HTML CON ESTILO HACKER
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre} // CV</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #050505;
            --bg-card: #0a0f0a;
            --green: #00ff41;
            --green-dim: #00aa2a;
            --cyan: #00ffff;
            --amber: #ffb000;
            --red: #ff2a2a;
            --text: #d0ffd8;
            --border: #003300;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @page {{
            size: A4;
            margin: 12mm;
        }}

        body {{
            font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.5;
            font-size: 8.8pt;
            padding: 0;
            margin: 0;
            position: relative;
            min-height: 100vh;
        }}

        body::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 255, 65, 0.03),
                rgba(0, 255, 65, 0.03) 1px,
                transparent 1px,
                transparent 3px
            );
            pointer-events: none;
            z-index: 1000;
        }}

        .container {{
            max-width: 186mm;
            margin: 0 auto;
            border: 1px solid var(--border);
            background: var(--bg-card);
            padding: 18px 22px;
            box-shadow: 0 0 25px rgba(0, 255, 65, 0.15), inset 0 0 40px rgba(0, 255, 65, 0.03);
            position: relative;
            box-sizing: border-box;
        }}

        .container::after {{
            content: "[ ENCRYPTED_TRANSMISSION :: TOP CLEARANCE ]";
            position: absolute;
            top: 4px;
            right: 12px;
            background: var(--bg);
            color: var(--red);
            font-size: 6.5pt;
            padding: 0 8px;
            border: 1px solid var(--red);
            letter-spacing: 1px;
        }}

        header {{
            text-align: center;
            border-bottom: 2px solid var(--green);
            padding-bottom: 14px;
            margin-bottom: 18px;
            position: relative;
            page-break-inside: avoid;
        }}

        .ascii-art {{
            color: var(--green-dim);
            font-size: 6pt;
            line-height: 1.15;
            margin-bottom: 8px;
            white-space: pre;
            text-align: center;
        }}

        h1 {{
            color: var(--green);
            font-size: 24pt;
            font-weight: 700;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.6);
            letter-spacing: 3px;
            margin-bottom: 4px;
            text-transform: uppercase;
        }}

        .handle {{
            color: var(--cyan);
            font-size: 10pt;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }}

        .contact {{
            color: var(--text);
            font-size: 8.5pt;
        }}

        .contact span {{
            margin: 0 8px;
            color: var(--green-dim);
        }}

        .repo {{
            color: var(--green-dim);
            font-size: 7.5pt;
            margin-top: 8px;
            letter-spacing: 0.5px;
        }}

        .repo a {{
            color: var(--cyan);
            text-decoration: none;
        }}

        h2 {{
            color: var(--green);
            font-size: 10.5pt;
            border-left: 4px solid var(--green);
            padding-left: 10px;
            margin: 16px 0 8px 0;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            display: flex;
            align-items: center;
            flex-wrap: nowrap;
            white-space: nowrap;
            page-break-after: avoid;
        }}

        h2::before {{
            content: "root@ortiz:~$ ";
            color: var(--cyan);
            margin-right: 8px;
            font-size: 10pt;
        }}

        h3 {{
            color: var(--cyan);
            font-size: 10pt;
            margin: 14px 0 6px 0;
            display: flex;
            align-items: center;
        }}

        h3::before {{
            content: "> ";
            color: var(--green);
        }}

        p {{
            margin-bottom: 10px;
            text-align: justify;
        }}

        .section {{
            margin-bottom: 14px;
            border: 1px solid var(--border);
            padding: 12px;
            background: rgba(0, 20, 0, 0.3);
            page-break-inside: avoid;
        }}

        ul {{
            list-style: none;
            padding-left: 0;
        }}

        ul li {{
            position: relative;
            padding-left: 18px;
            margin-bottom: 4px;
        }}

        ul li::before {{
            content: "[+]";
            position: absolute;
            left: 0;
            color: var(--green);
            font-size: 8pt;
        }}

        .two-col {{
            display: flex;
            gap: 20px;
        }}

        .col {{
            flex: 1;
        }}

        .skill-tag {{
            display: inline-block;
            border: 1px solid var(--green-dim);
            color: var(--green);
            padding: 2px 8px;
            margin: 2px;
            font-size: 7.5pt;
            background: rgba(0, 255, 65, 0.05);
        }}

        .project {{
            margin-bottom: 10px;
            border-left: 2px solid var(--cyan);
            padding-left: 10px;
            page-break-inside: avoid;
        }}

        .project-title {{
            color: var(--amber);
            font-weight: 600;
        }}

        .project-meta {{
            color: var(--green-dim);
            font-size: 8pt;
        }}

        .ref-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            font-size: 7.5pt;
        }}

        .ref-item {{
            border: 1px solid var(--border);
            padding: 6px;
            background: rgba(0, 30, 0, 0.3);
            page-break-inside: avoid;
        }}

        .ref-name {{
            color: var(--cyan);
            font-weight: 600;
        }}

        .status-line {{
            border-top: 1px solid var(--border);
            margin-top: 20px;
            padding-top: 8px;
            font-size: 7pt;
            color: var(--green-dim);
            text-align: center;
        }}

        .blink {{
            animation: blink 1s step-end infinite;
        }}

        @keyframes blink {{
            50% {{ opacity: 0; }}
        }}

        .highlight {{
            color: var(--amber);
        }}

        .dim {{
            color: var(--green-dim);
        }}

        @media print {{
            body {{
                padding: 0;
                background: var(--bg);
            }}
            body::before {{
                display: none;
            }}
            .container {{
                box-shadow: none;
                border: 1px solid var(--border);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="ascii-art">
    ____       _     _           _     
   |  _ \\  ___| | __| |_ __ _ __| |_  
   | | | |/ _ \\ |/ _` | '__| '__| __| 
   | |_| |  __/ | (_| | |  | |  | |_  
   |____/ \\___|_|\\__,_|_|  |_|   \\__| 
            </div>
            <h1>{nombre}</h1>
            <div class="handle">// {titulo} //</div>
            <div class="contact">
                {email} <span>//</span> {experiencia} <span>//</span> {ubicacion}
            </div>
            <div class="repo">
                [INFO] Este CV se actualiza a diario desde: <a href="{repo}">{repo}</a>
            </div>
        </header>

        {contenido}

        <div class="status-line">
            [EOF] {email} // root@ortiz:~$ _<span class="blink">&#9608;</span>
        </div>
    </div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# PARSER DEL ARCHIVO DE DATOS
# ---------------------------------------------------------------------------

def parse_cv_data(filepath):
    """Parsea cv_ortiz_datos.txt y retorna dict con metadatos y secciones."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = raw.splitlines()

    data = {
        "nombre": "",
        "titulo": "",
        "email": "",
        "experiencia": "",
        "ubicacion": "",
        "repo": "",
        "secciones": []
    }

    # Guardar copia de metadatos sin escapes para reemplazo en contenido
    raw_meta = {}


    # Metadatos al inicio del archivo: @clave valor
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("@"):
            key, _, value = line[1:].partition(" ")
            key = key.lower()
            val = value.strip()
            data[key] = val
            raw_meta[key] = val
            i += 1
        else:
            break

    # Secciones: [Nombre Sección]
    current_section = None
    current_project = None

    for line in lines[i:]:
        stripped = line.strip()

        if not stripped:
            # Línea en blanco: cierra descripción de proyecto si estaba abierto
            if current_project is not None:
                current_section["proyectos"].append(current_project)
                current_project = None
            continue

        if stripped.startswith("[") and stripped.endswith("]"):
            # Nueva sección
            if current_project is not None:
                current_section["proyectos"].append(current_project)
                current_project = None
            current_section = {
                "titulo": stripped[1:-1].strip(),
                "parrafos": [],
                "items": [],
                "proyectos": [],
                "skills": [],
                "tipo": "general"
            }
            data["secciones"].append(current_section)
            continue

        if current_section is None:
            # Ignorar líneas sueltas fuera de sección
            continue

        # Proyecto dentro de sección
        if stripped.startswith("# "):
            if current_project is not None:
                current_section["proyectos"].append(current_project)
            current_project = {
                "titulo": stripped[2:].strip(),
                "meta": "",
                "descripcion": ""
            }
            continue

        # Meta de proyecto
        if stripped.startswith("> "):
            if current_project is not None:
                current_project["meta"] = stripped[2:].strip()
            else:
                # Si aparece en sección de referencias como cargo
                current_section["items"].append(stripped[2:].strip())
            continue

        # Item de lista
        if stripped.startswith("- "):
            if current_project is not None:
                current_project["descripcion"] += " " + stripped[2:].strip()
            else:
                current_section["items"].append(stripped[2:].strip())
            continue

        # Skill tags (sección habilidades)
        if current_section["titulo"].lower() == "habilidades técnicas senior" and not stripped.startswith("+"):
            skills = stripped.split()
            current_section["skills"].extend(skills)
            continue

        # Texto suelto
        if current_project is not None:
            if current_project["descripcion"]:
                current_project["descripcion"] += " " + stripped
            else:
                current_project["descripcion"] = stripped
        else:
            current_section["parrafos"].append(stripped)

    # Agregar último proyecto si quedó pendiente
    if current_project is not None and current_section is not None:
        current_section["proyectos"].append(current_project)

    # Reemplazar @clave por el valor del metadato en todo el contenido
    replace_meta_tokens(data, raw_meta)

    return data


def replace_meta_tokens(data, raw_meta):
    """Sustituye referencias @clave por sus valores en párrafos, items y descripciones."""
    def replace_in_text(text):
        if not text:
            return text
        for key, value in raw_meta.items():
            text = text.replace(f"@{key}", value)
        return text

    for section in data["secciones"]:
        section["parrafos"] = [replace_in_text(p) for p in section["parrafos"]]
        section["items"] = [replace_in_text(item) for item in section["items"]]
        section["titulo"] = replace_in_text(section["titulo"])
        for project in section["proyectos"]:
            project["titulo"] = replace_in_text(project["titulo"])
            project["meta"] = replace_in_text(project["meta"])
            project["descripcion"] = replace_in_text(project["descripcion"])



# ---------------------------------------------------------------------------
# RENDERIZADO HTML
# ---------------------------------------------------------------------------

def html_escape(text):
    return escape(text)


def render_parrafo(texto):
    # Resaltar texto entre **
    texto = html_escape(texto)
    texto = re.sub(r'\*\*(.*?)\*\*', r'<span class="highlight">\1</span>', texto)
    return f"<p>{texto}</p>\n"


def render_item(item):
    item_html = html_escape(item)
    item_html = re.sub(r'\*\*(.*?)\*\*', r'<span class="highlight">\1</span>', item_html)
    return f"<li>{item_html}</li>\n"


def render_proyecto(project):
    html = '<div class="project">\n'
    html += f'    <div class="project-title">{html_escape(project["titulo"])}</div>\n'
    if project.get("meta"):
        html += f'    <div class="project-meta">{html_escape(project["meta"])}</div>\n'
    if project.get("descripcion"):
        desc = html_escape(project["descripcion"].strip())
        desc = re.sub(r'\*\*(.*?)\*\*', r'<span class="highlight">\1</span>', desc)
        html += f'    <p>{desc}</p>\n'
    html += '</div>\n'
    return html


def render_seccion(section):
    titulo = section["titulo"]
    html = f'<div class="section">\n'
    html += f'    <h2>{html_escape(titulo)}</h2>\n'

    # Habilidades técnicas
    if titulo.lower() == "habilidades técnicas senior":
        html += '    <div style="margin-bottom: 8px;">\n'
        for skill in section.get("skills", []):
            html += f'        <span class="skill-tag">{html_escape(skill)}</span>\n'
        html += '    </div>\n'
        for para in section["parrafos"]:
            html += f'    <p class="dim" style="font-size: 8pt; margin-top: 8px;">{html_escape(para)}</p>\n'
        html += '</div>\n'
        return html

    # Párrafos
    for para in section["parrafos"]:
        html += render_parrafo(para)

    # Items de lista
    if section["items"]:
        html += '    <ul>\n'
        for item in section["items"]:
            html += '        ' + render_item(item)
        html += '    </ul>\n'

    # Proyectos
    if section["proyectos"]:
        # Referencias en grid de 2 columnas
        if titulo.lower() == "referencias":
            html += '    <div class="ref-grid">\n'
            for project in section["proyectos"]:
                html += '        <div class="ref-item">\n'
                html += f'            <div class="ref-name">{html_escape(project["titulo"])}</div>\n'
                if project.get("meta"):
                    html += f'            {html_escape(project["meta"])}<br>\n'
                if project.get("descripcion"):
                    html += f'            {html_escape(project["descripcion"].strip())}\n'
                html += '        </div>\n'
            html += '    </div>\n'
        else:
            # Proyectos: algunos en dos columnas si son cortos
            proyectos = section["proyectos"]
            i = 0
            while i < len(proyectos):
                p = proyectos[i]
                desc_len = len(p.get("descripcion", ""))
                # Si el proyecto es corto y hay otro disponible, ponerlos en dos columnas
                if desc_len < 180 and i + 1 < len(proyectos):
                    p2 = proyectos[i + 1]
                    html += '    <div class="two-col">\n'
                    html += '        <div class="col">\n'
                    html += '            ' + render_proyecto(p).replace('\n', '\n            ')
                    html += '        </div>\n'
                    html += '        <div class="col">\n'
                    html += '            ' + render_proyecto(p2).replace('\n', '\n            ')
                    html += '        </div>\n'
                    html += '    </div>\n'
                    i += 2
                else:
                    html += '    ' + render_proyecto(p)
                    i += 1

    html += '</div>\n'
    return html


def render_html(data):
    contenido = ""
    for section in data["secciones"]:
        contenido += render_seccion(section)

    return HTML_TEMPLATE.format(
        nombre=html_escape(data.get("nombre", "")),
        titulo=html_escape(data.get("titulo", "")),
        email=html_escape(data.get("email", "")),
        experiencia=html_escape(data.get("experiencia", "")),
        ubicacion=html_escape(data.get("ubicacion", "")),
        repo=html_escape(data.get("repo", "")),
        contenido=contenido
    )


# ---------------------------------------------------------------------------
# GENERACIÓN PDF
# ---------------------------------------------------------------------------

def generate_pdf(html_path, pdf_path):
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        "--run-all-compositor-stages-before-draw",
        html_path
    ]
    print(f"Generando PDF: {pdf_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error al generar PDF:")
        print(result.stderr)
        return False
    print("PDF generado correctamente.")
    return True


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(DATA_FILE):
        print(f"No se encontró el archivo de datos: {DATA_FILE}")
        sys.exit(1)

    print(f"Leyendo datos desde: {DATA_FILE}")
    data = parse_cv_data(DATA_FILE)

    print(f"Generando HTML: {HTML_FILE}")
    html = render_html(data)
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    if not generate_pdf(HTML_FILE, PDF_FILE):
        sys.exit(1)

    print(f"\n✓ CV generado con éxito:")
    print(f"  HTML: {HTML_FILE}")
    print(f"  PDF:  {PDF_FILE}")


if __name__ == "__main__":
    main()
