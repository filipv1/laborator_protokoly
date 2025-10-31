"""
Test hranicinich pripadu pro jedenactou podminku.

Testuje PRESNE hodnoty (rovno 1/3 limitu, rovno limitu).
"""
import json
from core.text_generator import generate_conditional_texts

# Nacteme measurement_data
with open("measurement_data_example.json", "r", encoding="utf-8") as f:
    measurement_data = json.load(f)

# Spolecna tabulka W4_Y51
TABLE_W4_Y51 = {
    "1": {"fmax": "Fmax [N]", "phk": "PHK", "lhk": "LHK"},
    "2": {"fmax": 50, "phk": 12000, "lhk": 13000},
}

print("=" * 80)
print("HRANICNI PRIPADY - JEDENACTA PODMINKA")
print("=" * 80)
print("\nHygienicke limity:")
print("  PHK limit: 12000")
print("  LHK limit: 13000")
print("  1/3 PHK limitu: 4000")
print("  1/3 LHK limitu: 4333.33...")

# ============================================================================
# TEST: Hodnota ROVNA 1/3 limitu
# ============================================================================
print("\n" + "=" * 80)
print("TEST: HODNOTA ROVNA 1/3 LIMITU (4000 = 12000/3)")
print("=" * 80)

results_data_eq_third = {
    "Fmax_Phk_Extenzor": 50.0,
    "Fmax_Phk_Flexor": 50.0,
    "Fmax_Lhk_Extenzor": 50.0,
    "Fmax_Lhk_Flexor": 50.0,
    "phk_number_of_movements": 4000,  # PRESNE 1/3 limitu
    "lhk_number_of_movements": 3000,  # POD 1/3 limitu
    "table_W4_Y51": TABLE_W4_Y51
}

texts = generate_conditional_texts(measurement_data, results_data_eq_third)
result = texts.get("jedenacta_text_podminka", "N/A")

print(f"PHK pocet pohybu: {results_data_eq_third['phk_number_of_movements']} (= 1/3 limitu)")
print(f"LHK pocet pohybu: {results_data_eq_third['lhk_number_of_movements']} (< 1/3 limitu)")
print(f"\nVysledek: {result}")
print("Logika: 4000 > 4000/3 (1333.33) = True, ale 4000 <= 12000/3 (4000) = True")
print("Tzn. 4000 je <= 1/3 limitu, takze output musi byt '1'")

if result == "1":
    print("TEST PROSEL - hodnota ROVNA 1/3 limitu je stale POD limitem")
else:
    print(f"TEST SELHAL - ocekavano '1', ale dostano '{result}'")

# ============================================================================
# TEST: Hodnota ROVNA limitu
# ============================================================================
print("\n" + "=" * 80)
print("TEST: HODNOTA ROVNA LIMITU (12000)")
print("=" * 80)

results_data_eq_limit = {
    "Fmax_Phk_Extenzor": 50.0,
    "Fmax_Phk_Flexor": 50.0,
    "Fmax_Lhk_Extenzor": 50.0,
    "Fmax_Lhk_Flexor": 50.0,
    "phk_number_of_movements": 12000,  # PRESNE rovno limitu
    "lhk_number_of_movements": 3000,
    "table_W4_Y51": TABLE_W4_Y51
}

texts2 = generate_conditional_texts(measurement_data, results_data_eq_limit)
result2 = texts2.get("jedenacta_text_podminka", "N/A")

print(f"PHK pocet pohybu: {results_data_eq_limit['phk_number_of_movements']} (= limit)")
print(f"LHK pocet pohybu: {results_data_eq_limit['lhk_number_of_movements']} (< 1/3 limitu)")
print(f"\nVysledek: {result2}")
print("Logika: 12000 > 12000 = False (limit neni prekrocen)")
print("Ale: 12000 > 4000 (1/3 limitu) = True")
print("Tzn. output musi byt '2' (nad 1/3, ale neprekrocen limit)")

if result2 == "2":
    print("TEST PROSEL - hodnota ROVNA limitu je stale POD limitem (neprekracuje)")
else:
    print(f"TEST SELHAL - ocekavano '2', ale dostano '{result2}'")

# ============================================================================
# TEST: Hodnota TESNE nad limitem (12001)
# ============================================================================
print("\n" + "=" * 80)
print("TEST: HODNOTA TESNE NAD LIMITEM (12001)")
print("=" * 80)

results_data_over_limit = {
    "Fmax_Phk_Extenzor": 50.0,
    "Fmax_Phk_Flexor": 50.0,
    "Fmax_Lhk_Extenzor": 50.0,
    "Fmax_Lhk_Flexor": 50.0,
    "phk_number_of_movements": 12001,  # TESNE nad limitem
    "lhk_number_of_movements": 3000,
    "table_W4_Y51": TABLE_W4_Y51
}

texts3 = generate_conditional_texts(measurement_data, results_data_over_limit)
result3 = texts3.get("jedenacta_text_podminka", "N/A")

print(f"PHK pocet pohybu: {results_data_over_limit['phk_number_of_movements']} (> limit)")
print(f"LHK pocet pohybu: {results_data_over_limit['lhk_number_of_movements']} (< 1/3 limitu)")
print(f"\nVysledek: {result3}")
print("Logika: 12001 > 12000 = True (limit JE prekrocen)")
print("Tzn. output musi byt '3'")

if result3 == "3":
    print("TEST PROSEL - hodnota nad limitem = output '3'")
else:
    print(f"TEST SELHAL - ocekavano '3', ale dostano '{result3}'")

# ============================================================================
# SUMARIZACE
# ============================================================================
print("\n" + "=" * 80)
print("SUMARIZACE HRANICINICH PRIPADU")
print("=" * 80)

passed = 0
failed = 0

if result == "1":
    passed += 1
else:
    failed += 1

if result2 == "2":
    passed += 1
else:
    failed += 1

if result3 == "3":
    passed += 1
else:
    failed += 1

print(f"Proslo: {passed}/3")
print(f"Selhalo: {failed}/3")

if failed == 0:
    print("\n>>> VSECHNY HRANICNI PRIPADY PROSLY <<<")
else:
    print(f"\n>>> {failed} HRANICNI PRIPAD(Y) SELHALY <<<")
