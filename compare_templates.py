# -*- coding: utf-8 -*-
"""Porovná dvě Word šablony - najde rozdíly v placeholderech"""
import zipfile
import re
import sys
from pathlib import Path
from difflib import unified_diff

sys.stdout.reconfigure(encoding='utf-8')

broken_template = Path("Vzorové protokoly/Autorizované protokoly pro MUŽE/lsz_placeholdery_v2.docx")
working_template = Path("Vzorové protokoly/Autorizované protokoly pro MUŽE/lsz_placeholdery_v2 - Copy (14).docx")

print("POROVNANI SABLON")
print("=" * 80)
print(f"ROZBITA: {broken_template.name}")
print(f"FUNKCNI: {working_template.name}")
print("=" * 80)

# Extrahuj XML z obou šablon
with zipfile.ZipFile(broken_template, 'r') as zip_file:
    xml_broken = zip_file.read('word/document.xml').decode('utf-8')

with zipfile.ZipFile(working_template, 'r') as zip_file:
    xml_working = zip_file.read('word/document.xml').decode('utf-8')

# ANALÝZA 1: Balance závorek
print("\n1. BALANCE ZAVOREK:")
print("-" * 80)

broken_open = xml_broken.count('{{')
broken_close = xml_broken.count('}}')
working_open = xml_working.count('{{')
working_close = xml_working.count('}}')

print(f"ROZBITA:  {{ = {broken_open}, }} = {broken_close}, rozdil = {abs(broken_open - broken_close)}")
print(f"FUNKCNI:  {{ = {working_open}, }} = {working_close}, rozdil = {abs(working_open - working_close)}")

if broken_open != broken_close:
    print(f"\n[ERROR] Rozbita sablona ma NEBALANCOVANE zavorky!")
    print(f"        Chybi {abs(broken_open - broken_close)} zaviracich }}")

# ANALÝZA 2: Počet placeholderů
print("\n2. POCET PLACEHOLDERU:")
print("-" * 80)

pattern = r'\{\{[^}]*\}\}'
broken_placeholders = re.findall(pattern, xml_broken)
working_placeholders = re.findall(pattern, xml_working)

print(f"ROZBITA:  {len(broken_placeholders)} placeholderu")
print(f"FUNKCNI:  {len(working_placeholders)} placeholderu")
print(f"ROZDIL:   {abs(len(broken_placeholders) - len(working_placeholders))} placeholderu")

# ANALÝZA 3: Najdi neuzavřené placeholdery v rozbité
print("\n3. NEUZAVRENE PLACEHOLDERY V ROZBITE:")
print("-" * 80)

parts_broken = re.split(r'(\{\{|\}\})', xml_broken)
stack = []
open_positions = []

position = 0
for i, part in enumerate(parts_broken):
    if part == '{{':
        stack.append((position, i))
    elif part == '}}':
        if stack:
            stack.pop()
    position += len(part)

if stack:
    print(f"Nalezeno {len(stack)} neuzavrenych {{")
    for pos, token_idx in stack[-10:]:  # Posledních 10
        start = max(0, pos - 50)
        end = min(len(xml_broken), pos + 150)
        context = xml_broken[start:end]
        context_clean = re.sub(r'<[^>]+>', ' ', context)
        context_clean = ' '.join(context_clean.split())
        print(f"  Token #{token_idx}: {context_clean[:100]}")

# ANALÝZA 4: Najdi unikátní placeholdery (které jsou jen v jedné)
print("\n4. UNIKATNI PLACEHOLDERY:")
print("-" * 80)

# Extrahuj pouze názvy proměnných (bez XML tagů)
def extract_var_names(placeholders):
    var_names = set()
    for ph in placeholders:
        # Odstraň XML tagy
        clean = re.sub(r'<[^>]+>', '', ph)
        var_names.add(clean)
    return var_names

broken_vars = extract_var_names(broken_placeholders)
working_vars = extract_var_names(working_placeholders)

only_in_broken = broken_vars - working_vars
only_in_working = working_vars - broken_vars

if only_in_broken:
    print(f"\nJEN V ROZBITE ({len(only_in_broken)}):")
    for var in sorted(only_in_broken)[:20]:
        print(f"  - {var}")

if only_in_working:
    print(f"\nJEN VE FUNKCNI ({len(only_in_working)}):")
    for var in sorted(only_in_working)[:20]:
        print(f"  - {var}")

# ANALÝZA 5: Velikost souborů
print("\n5. VELIKOST SOUBORU:")
print("-" * 80)
print(f"ROZBITA:  {broken_template.stat().st_size:,} bytes")
print(f"FUNKCNI:  {working_template.stat().st_size:,} bytes")
print(f"ROZDIL:   {abs(broken_template.stat().st_size - working_template.stat().st_size):,} bytes")

# ANALÝZA 6: Délka XML
print("\n6. DELKA XML:")
print("-" * 80)
print(f"ROZBITA:  {len(xml_broken):,} znaku")
print(f"FUNKCNI:  {len(xml_working):,} znaku")
print(f"ROZDIL:   {abs(len(xml_broken) - len(xml_working)):,} znaku")

print("\n" + "=" * 80)
print("ANALYZA DOKONCENA")
