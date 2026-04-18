#!/usr/bin/env python3
"""Preprocess DERCAS.md for DOCX generation.

Cambios que aplica:
1. Extrae cada bloque ```mermaid``` a docs/diagrams/dNN.mmd.
2. Reemplaza cada bloque por una referencia URL al PNG en GitHub (no se embebe).
3. Elimina los separadores horizontales '---' decorativos que inflan páginas
   en DOCX (no afectan al MD renderizado en GitHub porque ahí se ven bien
   pero en Word generan líneas horizontales con espacio alrededor).
4. Prepende una portada APA básica con un salto de página OpenXML.
"""
import re
import os

SRC = "DERCAS.md"
OUT = "DERCAS-pre.md"
DIAGRAMS_DIR = "diagrams"
REPO_BASE = "https://github.com/AlexAlvarado1290/Proyecto-Analisis-de-sistemas/blob/main/docs/diagrams"
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

with open(SRC, encoding="utf-8") as f:
    content = f.read()

# 1-2: extraer y reemplazar bloques mermaid
pattern = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)
blocks = []
for m in pattern.finditer(content):
    blocks.append(m.group(1))

print(f"Found {len(blocks)} mermaid blocks")

for i, src in enumerate(blocks, 1):
    path = os.path.join(DIAGRAMS_DIR, f"d{i:02d}.mmd")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)

counter = {"i": 0}

def replace_mermaid(m):
    counter["i"] += 1
    n = f"{counter['i']:02d}"
    url = f"{REPO_BASE}/d{n}.png"
    return (
        f"> **Diagrama {counter['i']}** — disponible en el repositorio:\n"
        f"> [{url}]({url})\n"
    )

content = pattern.sub(replace_mermaid, content)

# 3: eliminar líneas que son solo '---' (separadores decorativos).
# Se conservan los '---' dentro de bloques de código (no aplican aquí) y los
# usados como línea de tabla (esos tienen '|', por eso el patrón es ^---$).
content = re.sub(r"\n---\n", "\n\n", content)

# Colapsar múltiples líneas en blanco consecutivas a máximo dos
content = re.sub(r"\n{3,}", "\n\n", content)

# 4: portada APA con salto de página OpenXML
portada = (
    "::: {custom-style=\"Portada\"}\n\n"
    "UNIVERSIDAD MARIANO GÁLVEZ DE GUATEMALA\n\n"
    "FACULTAD DE INGENIERÍA EN SISTEMAS\n\n"
    "ANÁLISIS DE SISTEMAS I\n\n"
    "PROYECTO II — DERCAS\n\n"
    "Sistema de Gestión y Comercialización Agrícola \"La Esperanza\"\n\n"
    "Alex Alvarado\n\n"
    "Guatemala, 17 de abril de 2026\n\n"
    ":::\n\n"
    "```{=openxml}\n"
    "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n"
    "```\n\n"
)

content = portada + content

with open(OUT, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Wrote {OUT}")
