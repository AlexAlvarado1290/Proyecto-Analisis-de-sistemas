#!/usr/bin/env python3
"""Preprocess DERCAS.md to replace mermaid blocks with external URL links.

Los diagramas se alojan en GitHub y se referencian por URL en el DOCX
para evitar embeber imágenes y mantener el documento compacto.
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

def replace(m):
    counter["i"] += 1
    n = f"{counter['i']:02d}"
    url = f"{REPO_BASE}/d{n}.png"
    return (
        f"> **Diagrama {counter['i']}** — disponible en el repositorio:\n"
        f"> [{url}]({url})\n"
        f">\n"
        f"> *(El archivo fuente Mermaid correspondiente está en `docs/diagrams/d{n}.mmd`.)*\n"
    )

new_content = pattern.sub(replace, content)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Wrote {OUT}")
