# -*- coding: utf-8 -*-
"""Najde neúplné placeholdery v Word šabloně"""
import zipfile
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

template_path = Path("Vzorové protokoly/Autorizované protokoly pro MUŽE/lsz_placeholdery_v2.docx")

with zipfile.ZipFile(template_path, 'r') as zip_file:
    xml_content = zip_file.read('word/document.xml').decode('utf-8')

print("Hledam neuzavrene {{ placeholdery...")
print("=" * 80)

# Rozděl XML na tokeny podle {{ a }}
parts = re.split(r'(\{\{|\}\})', xml_content)

# Sleduj otevřené/zavřené závorky
stack = []
open_positions = []
errors = []

position = 0
for i, part in enumerate(parts):
    if part == '{{':
        stack.append(position)
        open_positions.append((position, i))
    elif part == '}}':
        if stack:
            stack.pop()
        else:
            errors.append(f"Extra }} na pozici {position} (token #{i})")

    position += len(part)

# Pokud stack není prázdný, máme neuzavřené placeholdery
if stack:
    print(f"[ERROR] Nalezeno {len(stack)} neuzavrenych placeholderu!\n")

    for pos, token_idx in open_positions[-len(stack):]:  # Poslední neuzavřené
        # Extrahuj kontext kolem chyby
        start = max(0, pos - 100)
        end = min(len(xml_content), pos + 200)
        context = xml_content[start:end]

        # Odstraň XML tagy pro lepší čitelnost
        context_clean = re.sub(r'<[^>]+>', ' ', context)
        context_clean = ' '.join(context_clean.split())  # Normalize whitespace

        print(f"Token #{token_idx}, pozice {pos}:")
        print(f"  Kontext: ...{context_clean[:150]}...")
        print()

if errors:
    print("[ERROR] Extra }} zavorky:")
    for err in errors:
        print(f"  {err}")

if not stack and not errors:
    print("[OK] Vsechny placeholdery jsou spravne uzavrene")

print(f"\nCelkem {{ v dokumentu: {xml_content.count('{{')}")
print(f"Celkem }} v dokumentu: {xml_content.count('}}')}")
print(f"Rozdil: {abs(xml_content.count('{{') - xml_content.count('}}'))}")
