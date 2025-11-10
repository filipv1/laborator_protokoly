"""
Test PP limitů na reálných datech z projektu _fjfjfe
"""
import json
from pathlib import Path
from core.text_generator import generate_conditional_texts

# Načti measurement_data.json
project_path = Path("projects/_fjfjfe")
measurement_data_path = project_path / "measurement_data.json"

print("="*60)
print("TEST: PP limity na reálných datech")
print("="*60)
print()

with open(measurement_data_path, 'r', encoding='utf-8') as f:
    measurement_data = json.load(f)

# Přidej work_duration_min pro test (standardní směna)
if "work_duration_min" not in measurement_data.get("section3_additional_data", {}):
    print("[INFO] work_duration_min chybi -> pouzije se fallback 480 min")
    print()

# Vygeneruj podmínkové texty pro PP
texts = generate_conditional_texts(
    measurement_data=measurement_data,
    results_data=None,  # PP nepotřebuje results pro limity
    protocol_type="PP_CAS"
)

print()
print("="*60)
print("VYGENEROVANÉ LIMITY:")
print("="*60)
print()
print(f"pp_kat1_min:  {texts.get('pp_kat1_min')}")
print(f"pp_kat1_max:  {texts.get('pp_kat1_max')}")
print(f"pp_kat2_min:  {texts.get('pp_kat2_min')}")
print(f"pp_kat2_max:  {texts.get('pp_kat2_max')}")
print(f"pp_kat3_min:  {texts.get('pp_kat3_min')}")
print()
print(f"n_kat1_min:   {texts.get('n_kat1_min')}")
print(f"n_kat1_max:   {texts.get('n_kat1_max')}")
print(f"n_kat2_min:   {texts.get('n_kat2_min')}")
print(f"n_kat2_max:   {texts.get('n_kat2_max')}")
print(f"n_kat3_min:   {texts.get('n_kat3_min')}")
print()
print("="*60)
print("[OK] Test dokoncen - limity jsou pripraveny pro Word sablony")
print("="*60)
