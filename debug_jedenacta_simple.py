"""
Simple debug - jen kontrola klicu
"""
import json
from core.text_generator import generate_conditional_texts

# Nacti data
with open("measurement_data_example.json", "r", encoding="utf-8") as f:
    measurement_data = json.load(f)

with open("lsz_results.json", "r", encoding="utf-8") as f:
    results_data = json.load(f)

print("Generuji podminky...")
texts = generate_conditional_texts(measurement_data, results_data)

print("\nVSECHNY KLICE V texts:")
print("=" * 60)
for key in sorted(texts.keys()):
    print(f"  - {key}")

print("\n" + "=" * 60)
print("HLEDAME: jedenacta_text_podminka")
print("=" * 60)

if "jedenacta_text_podminka" in texts:
    value = texts["jedenacta_text_podminka"]
    print(f"NALEZENO!")
    print(f"Hodnota: {value}")
    print(f"Typ: {type(value)}")
    if value == "":
        print("PROBLEM: Hodnota je prazdny string!")
    elif value is None:
        print("PROBLEM: Hodnota je None!")
else:
    print("PROBLEM: Klic jedenacta_text_podminka NENALEZEN!")

# Manualni test
print("\n" + "=" * 60)
print("MANUALNI VOLANI FUNKCE:")
print("=" * 60)

from core.text_generator import _calculate_jedenacta_text_podminka

result = _calculate_jedenacta_text_podminka(results_data)
print(f"Vysledek: {result}")
print(f"Typ: {type(result)}")
