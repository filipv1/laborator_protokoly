"""
Test osmé podmínky s REÁLNÝMI daty z projektu 222_rentury
"""
import sys
import os
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from core.text_generator import generate_conditional_texts


# Načti reálná data
with open(r"C:\Users\vaclavik\lab3\laborator_protokoly\projects\222_rentury\measurement_data.json", encoding='utf-8') as f:
    measurement_data = json.load(f)

with open(r"C:\Users\vaclavik\lab3\laborator_protokoly\projects\222_rentury\lsz_results.json", encoding='utf-8') as f:
    results_data = json.load(f)

# Vygeneruj všechny conditional texts
texts = generate_conditional_texts(measurement_data, results_data)

print("=" * 80)
print("TEST: Osmá podmínka s REÁLNÝMI daty (projekt 222_rentury)")
print("=" * 80)

print("\n📊 ANALÝZA DAT:")
print("-" * 80)

# Zkontroluj řádek 21 (Celkem)
row_21 = results_data["table_force_distribution"]["21"]
print(f"\nŘádek 21 (Celkem):")
print(f"  force_over_70_phk_extenzory: {row_21['force_over_70_phk_extenzory']}")
print(f"  force_over_70_phk_flexory: {row_21['force_over_70_phk_flexory']}")
print(f"  force_over_70_lhk_extenzory: {row_21['force_over_70_lhk_extenzory']}")
print(f"  force_over_70_lhk_flexory: {row_21['force_over_70_lhk_flexory']}")

max_val = max(
    row_21['force_over_70_phk_extenzory'],
    row_21['force_over_70_phk_flexory'],
    row_21['force_over_70_lhk_extenzory'],
    row_21['force_over_70_lhk_flexory']
)
print(f"\n  Maximální hodnota: {max_val}")
print(f"  Je > 100? {max_val > 100}")

# Zkontroluj konkrétní činnosti
print("\n\nKonkrétní činnosti s force_over_70 > 100:")
print("-" * 80)
activities_found = []
for key, row in results_data["table_force_distribution"].items():
    if key == "21":  # Skip Celkem
        continue

    activity = row.get("activity")
    if not activity or activity == 0:
        continue

    # Zkontroluj všechny 4 hodnoty
    values = [
        row.get("force_over_70_phk_extenzory", 0),
        row.get("force_over_70_phk_flexory", 0),
        row.get("force_over_70_lhk_extenzory", 0),
        row.get("force_over_70_lhk_flexory", 0)
    ]

    # Konvertuj None na 0
    values = [v if v is not None else 0 for v in values]
    max_in_row = max(values)

    if max_in_row > 100:
        print(f"\n  Řádek {key}: {activity}")
        print(f"    PHK ext: {values[0]}, PHK flex: {values[1]}")
        print(f"    LHK ext: {values[2]}, LHK flex: {values[3]}")
        print(f"    Maximum: {max_in_row} > 100 ✓")
        activities_found.append(activity)

print("\n" + "=" * 80)
print("🎯 VYGENEROVANÉ CONDITIONAL TEXTS:")
print("=" * 80)

for key, value in texts.items():
    if key == "osmy_text_podminka":
        print(f"\n⭐ {key}:")
        print(f"   '{value}'")
    else:
        print(f"\n{key}:")
        if len(str(value)) > 70:
            print(f"   {str(value)[:70]}...")
        else:
            print(f"   {value}")

print("\n" + "=" * 80)
print("✅ VÝSLEDEK:")
print("=" * 80)

expected = ", ".join(activities_found) if activities_found else ""
actual = texts.get("osmy_text_podminka", "")

print(f"\nOčekáváno: '{expected}'")
print(f"Skutečnost: '{actual}'")

if expected == actual:
    print("\n🎉 ÚSPĚCH! Osmá podmínka funguje správně!")
else:
    print(f"\n❌ CHYBA! Neshoduje se!")
    print(f"   Očekávané činnosti: {activities_found}")

print("\n" + "=" * 80)
