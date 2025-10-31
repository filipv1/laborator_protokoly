"""
Test pro desátou podmínku - všechny hodnoty POD limitem.
"""
import json
from core.text_generator import generate_conditional_texts

# Načti testovací data
with open("measurement_data_example.json", "r", encoding="utf-8") as f:
    measurement_data = json.load(f)

# Vytvoř testovací results_data s NÍZKÝMI počty pohybů (POD limitem)
results_data = {
    "Fmax_Phk_Extenzor": 50.5,
    "Fmax_Phk_Flexor": 45.3,
    "Fmax_Lhk_Extenzor": 48.7,
    "Fmax_Lhk_Flexor": 43.2,
    "phk_number_of_movements": 8000,   # POD limitem (12500)
    "lhk_number_of_movements": 9000,   # POD limitem (13500)
    "table_W4_Y51": {
        "1": {"fmax": "Fmax [N]", "phk": "PHK", "lhk": "LHK"},
        "2": {"fmax": 50, "phk": 12500, "lhk": 13000},
        "3": {"fmax": 45, "phk": 13500, "lhk": 14000},
        "4": {"fmax": 48, "phk": 13000, "lhk": 13500},
        "5": {"fmax": 43, "phk": 14000, "lhk": 14500}
    }
}

# Vygeneruj podmínkové texty
texts = generate_conditional_texts(measurement_data, results_data)

# Výsledky
print("=" * 80)
print("TEST: VSECHNY HODNOTY POD LIMITEM")
print("=" * 80)
print(f"PHK pocet pohybu: {results_data['phk_number_of_movements']}")
print(f"LHK pocet pohybu: {results_data['lhk_number_of_movements']}")

print("\n" + "=" * 80)
print("DEVATA PODMINKA (jednotlive svalove skupiny):")
print("=" * 80)
devata = texts.get("devata_text_podminka", {})
print(f"PHK Extenzory: {devata.get('phk_extenzory', 'N/A')}")
print(f"PHK Flexory:   {devata.get('phk_flexory', 'N/A')}")
print(f"LHK Extenzory: {devata.get('lhk_extenzory', 'N/A')}")
print(f"LHK Flexory:   {devata.get('lhk_flexory', 'N/A')}")

print("\n" + "=" * 80)
print("DESATA PODMINKA (celkove prekroceni):")
print("=" * 80)
desata = texts.get("desata_text_podminka", "N/A")
print(f"Vysledek: {desata}")

print("\n" + "=" * 80)
print("OCEKAVANY VYSLEDEK: 'Pod limitem'")
print("=" * 80)
if desata == "Pod limitem":
    print("TEST PROSEL - vsechny hodnoty jsou pod limitem")
else:
    print("TEST SELHAL - ocekavano 'Pod limitem', ale dostano '{}'".format(desata))
