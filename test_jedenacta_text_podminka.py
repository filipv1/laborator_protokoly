"""
Test pro jedenactou podminku - hierarchicke vyhodnoceni zatizeni vsech svalovych skupin.

Testuje 3 scenare:
1. Output "1" - zadny sval neni nad 1/3 hygienickeho limitu
2. Output "2" - alespon jeden sval je nad 1/3 limitu, ale zadny neprekracuje limit
3. Output "3" - alespon jeden sval prekracuje hygienicky limit
"""
import json
from core.text_generator import generate_conditional_texts

# Nacteme measurement_data (pro kontext, ale neni nutne pro tuto podminku)
with open("measurement_data_example.json", "r", encoding="utf-8") as f:
    measurement_data = json.load(f)

# Spolecna tabulka W4_Y51 pro vsechny testy
TABLE_W4_Y51 = {
    "1": {"fmax": "Fmax [N]", "phk": "PHK", "lhk": "LHK"},
    "2": {"fmax": 50, "phk": 12000, "lhk": 13000},  # PHK limit: 12000, LHK limit: 13000
    "3": {"fmax": 45, "phk": 13500, "lhk": 14000},
    "4": {"fmax": 48, "phk": 13000, "lhk": 13500},
    "5": {"fmax": 43, "phk": 14000, "lhk": 14500}
}

print("=" * 80)
print("TEST JEDENACTE PODMINKY - HIERARCHICKE VYHODNOCENI ZATIZENI")
print("=" * 80)
print("\nHygienicke limity (z tabulky W4_Y51):")
print("  PHK limit pro Fmax=50: 12000 pohybu")
print("  LHK limit pro Fmax=48: 13000 pohybu")
print("  1/3 PHK limitu: 4000 pohybu")
print("  1/3 LHK limitu: 4333 pohybu")

# ============================================================================
# TEST 1: Vsechny svaly POD 1/3 limitu -> Output "1"
# ============================================================================
print("\n" + "=" * 80)
print("TEST 1: VSECHNY SVALY POD 1/3 LIMITU")
print("=" * 80)

results_data_test1 = {
    "Fmax_Phk_Extenzor": 50.0,  # Limit: 12000, 1/3: 4000
    "Fmax_Phk_Flexor": 50.0,    # Limit: 12000, 1/3: 4000
    "Fmax_Lhk_Extenzor": 48.0,  # Limit: 13000, 1/3: 4333
    "Fmax_Lhk_Flexor": 48.0,    # Limit: 13000, 1/3: 4333
    "phk_number_of_movements": 3000,  # POD 1/3 limitu (4000)
    "lhk_number_of_movements": 3000,  # POD 1/3 limitu (4333)
    "table_W4_Y51": TABLE_W4_Y51
}

texts1 = generate_conditional_texts(measurement_data, results_data_test1)
result1 = texts1.get("jedenacta_text_podminka", "N/A")

print(f"PHK pocet pohybu: {results_data_test1['phk_number_of_movements']}")
print(f"LHK pocet pohybu: {results_data_test1['lhk_number_of_movements']}")
print(f"\nVysledek: {result1}")
print(f"Ocekavano: 1")

if result1 == "1":
    print("TEST 1 PROSEL")
else:
    print(f"TEST 1 SELHAL - ocekavano '1', ale dostano '{result1}'")

# ============================================================================
# TEST 2: Alespon jeden sval NAD 1/3 limitu, ale POD limitem -> Output "2"
# ============================================================================
print("\n" + "=" * 80)
print("TEST 2: ALESPON JEDEN SVAL NAD 1/3 LIMITU, ALE POD LIMITEM")
print("=" * 80)

results_data_test2 = {
    "Fmax_Phk_Extenzor": 50.0,  # Limit: 12000, 1/3: 4000
    "Fmax_Phk_Flexor": 50.0,
    "Fmax_Lhk_Extenzor": 48.0,  # Limit: 13000, 1/3: 4333
    "Fmax_Lhk_Flexor": 48.0,
    "phk_number_of_movements": 8000,  # NAD 1/3 limitu (4000), ale POD limitem (12000)
    "lhk_number_of_movements": 3000,  # POD 1/3 limitu
    "table_W4_Y51": TABLE_W4_Y51
}

texts2 = generate_conditional_texts(measurement_data, results_data_test2)
result2 = texts2.get("jedenacta_text_podminka", "N/A")

print(f"PHK pocet pohybu: {results_data_test2['phk_number_of_movements']} (NAD 1/3 limitu: 4000, POD limitem: 12000)")
print(f"LHK pocet pohybu: {results_data_test2['lhk_number_of_movements']} (POD 1/3 limitu: 4333)")
print(f"\nVysledek: {result2}")
print(f"Ocekavano: 2")

if result2 == "2":
    print("TEST 2 PROSEL")
else:
    print(f"TEST 2 SELHAL - ocekavano '2', ale dostano '{result2}'")

# ============================================================================
# TEST 3: Alespon jeden sval NAD limitem -> Output "3"
# ============================================================================
print("\n" + "=" * 80)
print("TEST 3: ALESPON JEDEN SVAL NAD LIMITEM")
print("=" * 80)

results_data_test3 = {
    "Fmax_Phk_Extenzor": 50.0,  # Limit: 12000
    "Fmax_Phk_Flexor": 50.0,
    "Fmax_Lhk_Extenzor": 48.0,  # Limit: 13000
    "Fmax_Lhk_Flexor": 48.0,
    "phk_number_of_movements": 3000,   # POD limitem
    "lhk_number_of_movements": 15000,  # NAD limitem (13000)
    "table_W4_Y51": TABLE_W4_Y51
}

texts3 = generate_conditional_texts(measurement_data, results_data_test3)
result3 = texts3.get("jedenacta_text_podminka", "N/A")

print(f"PHK pocet pohybu: {results_data_test3['phk_number_of_movements']} (POD limitem: 12000)")
print(f"LHK pocet pohybu: {results_data_test3['lhk_number_of_movements']} (NAD limitem: 13000)")
print(f"\nVysledek: {result3}")
print(f"Ocekavano: 3")

if result3 == "3":
    print("TEST 3 PROSEL")
else:
    print(f"TEST 3 SELHAL - ocekavano '3', ale dostano '{result3}'")

# ============================================================================
# SUMARIZACE
# ============================================================================
print("\n" + "=" * 80)
print("SUMARIZACE TESTU")
print("=" * 80)

passed = 0
failed = 0

if result1 == "1":
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
    print("\n>>> VSECHNY TESTY PROSLY <<<")
else:
    print(f"\n>>> {failed} TEST(Y) SELHALY <<<")

print("\n" + "=" * 80)
print("POUZITI V WORD SABLONE:")
print("=" * 80)
print("{{ section_generated_texts.jedenacta_text_podminka }}")
print("\nVrati: '1', '2' nebo '3'")
