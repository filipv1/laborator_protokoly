# -*- coding: utf-8 -*-
"""Zkontroluje Jinja2 syntax v Word šabloně"""
import zipfile
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

template_path = Path("Vzorové protokoly/Autorizované protokoly pro MUŽE/lsz_placeholdery_v2.docx")

print(f"Kontroluji sablonu: {template_path}")
print("=" * 80)

with zipfile.ZipFile(template_path, 'r') as zip_file:
    xml_content = zip_file.read('word/document.xml').decode('utf-8')

# Hledej ROZBITÉ placeholdery
broken_patterns = [
    (r'\}\}\}', 'Extra }}} (tri zaviraci zavorky)'),
    (r'\{\{\{', 'Extra {{{ (tri otviraci zavorky)'),
    (r'%\}\}', 'Spatne uzavreni %}}'),
    (r'\{\{%', 'Spatne otevreni {{%'),
]

print("\nHledam rozbite placeholdery:")
print("-" * 80)

found_broken = False
for pattern, description in broken_patterns:
    matches = re.findall(pattern, xml_content)
    if matches:
        found_broken = True
        print(f"[ERROR] {description}: nalezeno {len(matches)}x")
        for match in matches[:5]:
            print(f"   {match}")

if not found_broken:
    print("[OK] Zadne zrejme chyby nenalezeny v zakladnich patternu")

# Najdi všechny {{ }} placeholdery
print("\nVsechny {{ }} placeholdery:")
print("-" * 80)
pattern1 = r'\{\{[^}]*\}\}'
matches1 = re.findall(pattern1, xml_content)
print(f"Celkem nalezeno: {len(matches1)} placeholderu")

# Zobraz prvnich 10
for i, match in enumerate(matches1[:10], 1):
    print(f"{i}. {match[:80]}")  # Max 80 chars

# Zkontroluj balance závorek v celém dokumentu
open_curly = xml_content.count('{{')
close_curly = xml_content.count('}}')
print(f"\nBalance zavorek:")
print(f"  Otviracich {{{{}}: {open_curly}")
print(f"  Zaviracich }}}}: {close_curly}")
if open_curly != close_curly:
    print(f"  [ERROR] NEBALANCOVANE! Rozdil: {abs(open_curly - close_curly)}")
else:
    print(f"  [OK] Balanc OK")

print(f"\nXML obsahuje {xml_content.count(chr(10))} radku (chyba byla na radku 730)")
