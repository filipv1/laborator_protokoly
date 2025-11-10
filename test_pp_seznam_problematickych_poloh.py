"""
Test nového placeholderu: pp_problematicke_polohy_seznam
Vrací POUZE seznam problematických poloh bez celého textu
"""
import sys
import json
from pathlib import Path
from core.text_generator import generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Načti data
project_path = Path("projects/_fjfjfe")
measurement_data_path = project_path / "measurement_data.json"
pp_results_path = project_path / "pp_results.json"

print("="*80)
print("TEST: PP seznam problematických poloh (nový placeholder)")
print("="*80)
print()

with open(measurement_data_path, 'r', encoding='utf-8') as f:
    measurement_data = json.load(f)

with open(pp_results_path, 'r', encoding='utf-8') as f:
    pp_results = json.load(f)

# Generovat podmínkové texty
texts = generate_conditional_texts(
    measurement_data=measurement_data,
    results_data=pp_results,
    protocol_type="PP_CAS"
)

print()
print("="*80)
print("VÝSLEDKY:")
print("="*80)
print()

# 1. Kompletní text s kategorizací
print("1. KOMPLETNÍ TEXT (prvni_pp_podminka_kategorie):")
print("-" * 80)
print(texts["prvni_pp_podminka_kategorie"])
print()

# 2. NOVÝ PLACEHOLDER - pouze seznam
print("2. NOVÝ PLACEHOLDER - POUZE SEZNAM (pp_problematicke_polohy_seznam):")
print("-" * 80)
if texts["pp_problematicke_polohy_seznam"]:
    print(texts["pp_problematicke_polohy_seznam"])
else:
    print("(prázdný - žádné problémy, vše v kategorii 1)")
print()

# 3. Použití v Word šabloně
print("3. POUŽITÍ V WORD ŠABLONĚ:")
print("-" * 80)
print("Varianta A - Kompletní text:")
print("  {{ texts.prvni_pp_podminka_kategorie }}")
print()
print("Varianta B - Vlastní formulace + seznam:")
print('  Problematické polohy: {{ texts.pp_problematicke_polohy_seznam }}')
print()
print('  {% if texts.pp_problematicke_polohy_seznam %}')
print('    Překročení limitů u: {{ texts.pp_problematicke_polohy_seznam }}')
print('  {% else %}')
print('    Všechny polohy v kategorii 1 (bez problémů)')
print('  {% endif %}')
print()

# 4. Kategoriální limity
print("4. KATEGORIÁLNÍ LIMITY (pro referenci):")
print("-" * 80)
print(f"PP kategorie 1: 0-{texts['pp_kat1_max']} min")
print(f"PP kategorie 2: {texts['pp_kat2_min']}-{texts['pp_kat2_max']} min")
print(f"PP kategorie 3: >{texts['pp_kat3_min']} min")
print()
print(f"N kategorie 1: 0-{texts['n_kat1_max']} min")
print(f"N kategorie 2: {texts['n_kat2_min']}-{texts['n_kat2_max']} min")
print(f"N kategorie 3: >{texts['n_kat3_min']} min")
print()

print("="*80)
print("TEST DOKONČEN")
print("="*80)
