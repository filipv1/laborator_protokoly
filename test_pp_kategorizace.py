"""
Test PP kategorizace pracovnich poloh na realnych datech
"""
import json
from pathlib import Path
from core.text_generator import generate_conditional_texts

# Nacti data
project_path = Path("projects/_fjfjfe")
measurement_data_path = project_path / "measurement_data.json"
pp_results_path = project_path / "pp_results.json"

print("="*70)
print("TEST: PP kategorizace pracovnich poloh")
print("="*70)
print()

with open(measurement_data_path, 'r', encoding='utf-8') as f:
    measurement_data = json.load(f)

with open(pp_results_path, 'r', encoding='utf-8') as f:
    pp_results = json.load(f)

print(f"[INFO] Nacteno {len(pp_results.get('trup', {}))} poloh z sekce 'trup'")
print(f"[INFO] Nacteno {len(pp_results.get('hlava_krk', {}))} poloh z sekce 'hlava_krk'")
print(f"[INFO] Nacteno {len(pp_results.get('phk', {}))} poloh z sekce 'phk'")
print(f"[INFO] Nacteno {len(pp_results.get('lhk', {}))} poloh z sekce 'lhk'")
print(f"[INFO] Nacteno {len(pp_results.get('dk', {}))} poloh z sekce 'dk'")
print(f"[INFO] Nacteno {len(pp_results.get('ostatni', {}))} poloh z sekce 'ostatni'")
print()

# Vygeneruj podminko ve texty
texts = generate_conditional_texts(
    measurement_data=measurement_data,
    results_data=pp_results,
    protocol_type="PP_CAS"
)

print()
print("="*70)
print("VYSLEDEK KATEGORIZACE:")
print("="*70)
print()
print(f"Prvni PP podminka kategorie:")
print(f"  {texts.get('prvni_pp_podminka_kategorie', 'N/A')}")
print()
print("="*70)
print("[OK] Test dokoncen")
print("="*70)
