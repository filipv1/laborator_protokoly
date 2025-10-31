"""
DEBUG pro jedenactou podminku - zjisti, proc se placeholder v Word neukaze.
"""
import json
from core.text_generator import generate_conditional_texts

print("=" * 80)
print("DEBUG - JEDENACTA PODMINKA")
print("=" * 80)

# Nacti measurement_data
print("\n1. Nacitam measurement_data.json...")
try:
    with open("measurement_data_example.json", "r", encoding="utf-8") as f:
        measurement_data = json.load(f)
    print("   OK - measurement_data nacten")
except Exception as e:
    print(f"   CHYBA: {e}")
    measurement_data = {}

# Nacti results_data
print("\n2. Nacitam lsz_results.json...")
try:
    with open("lsz_results.json", "r", encoding="utf-8") as f:
        results_data = json.load(f)
    print("   OK - results_data nacten")

    # Vypis dulezita data
    print("\n   Dulezita data z results_data:")
    print(f"   - Fmax_Phk_Extenzor: {results_data.get('Fmax_Phk_Extenzor')}")
    print(f"   - Fmax_Phk_Flexor: {results_data.get('Fmax_Phk_Flexor')}")
    print(f"   - Fmax_Lhk_Extenzor: {results_data.get('Fmax_Lhk_Extenzor')}")
    print(f"   - Fmax_Lhk_Flexor: {results_data.get('Fmax_Lhk_Flexor')}")
    print(f"   - phk_number_of_movements: {results_data.get('phk_number_of_movements')}")
    print(f"   - lhk_number_of_movements: {results_data.get('lhk_number_of_movements')}")
    print(f"   - table_W4_Y51 pritomna: {bool(results_data.get('table_W4_Y51'))}")

except FileNotFoundError:
    print("   CHYBA: Soubor lsz_results.json nenalezen!")
    print("   Vytvarim testovaci data...")
    results_data = {
        "Fmax_Phk_Extenzor": 50.5,
        "Fmax_Phk_Flexor": 45.3,
        "Fmax_Lhk_Extenzor": 48.7,
        "Fmax_Lhk_Flexor": 43.2,
        "phk_number_of_movements": 15000,
        "lhk_number_of_movements": 14000,
        "table_W4_Y51": {
            "1": {"fmax": "Fmax [N]", "phk": "PHK", "lhk": "LHK"},
            "2": {"fmax": 50, "phk": 12500, "lhk": 13000},
            "3": {"fmax": 45, "phk": 13500, "lhk": 14000},
            "4": {"fmax": 48, "phk": 13000, "lhk": 13500},
            "5": {"fmax": 43, "phk": 14000, "lhk": 14500}
        }
    }
except Exception as e:
    print(f"   CHYBA: {e}")
    results_data = None

# Generuj podminky
print("\n3. Generuji podminky...")
texts = generate_conditional_texts(measurement_data, results_data)

print("\n4. VYSLEDKY - VSECHNY VYGENEROVANE PODMINKY:")
print("=" * 80)

# Vypis VSECHNY klice (bez vypisu dlouhych textu, jen klice a typy)
for key, value in sorted(texts.items()):
    if isinstance(value, dict):
        print(f"\n{key}: [DICT s {len(value)} polozkami]")
        for subkey in value.keys():
            print(f"  - {subkey}")
    elif isinstance(value, str):
        if len(value) > 100:
            print(f"\n{key}: [STRING delka {len(value)}] {value[:50]}...")
        else:
            print(f"\n{key}: {repr(value)}")
    else:
        print(f"\n{key}: {type(value)} = {value}")

# Specialni kontrola jedenacte podminky
print("\n" + "=" * 80)
print("5. SPECIALNI KONTROLA - JEDENACTA PODMINKA:")
print("=" * 80)

jedenacta = texts.get("jedenacta_text_podminka")

if jedenacta is None:
    print("PROBLEM: jedenacta_text_podminka je None!")
    print("Mozne priciny:")
    print("  - Funkce _calculate_jedenacta_text_podminka() neni volana")
    print("  - results_data je None")
    print("  - Funkce vraci None misto '1', '2' nebo '3'")
elif jedenacta == "":
    print("PROBLEM: jedenacta_text_podminka je prazdny string!")
else:
    print(f"OK: jedenacta_text_podminka = '{jedenacta}'")
    print(f"Typ: {type(jedenacta)}")
    print(f"Delka: {len(jedenacta)}")

# Zkontroluj, jestli results_data bylo predano
print("\n6. KONTROLA PREDANI DAT:")
print("=" * 80)
print(f"results_data je None: {results_data is None}")
print(f"results_data je prazdny: {not results_data}")

# Zkus manualne zavolat funkci
print("\n7. MANUALNI VOLANI FUNKCE:")
print("=" * 80)

if results_data is not None:
    from core.text_generator import _calculate_jedenacta_text_podminka

    try:
        manual_result = _calculate_jedenacta_text_podminka(results_data)
        print(f"Manualni volani vraci: '{manual_result}'")
        print(f"Typ: {type(manual_result)}")
    except Exception as e:
        print(f"CHYBA pri manualnim volani: {e}")
        import traceback
        traceback.print_exc()
else:
    print("results_data je None, nelze manualne zavolat funkci")

# Vypis placeholder pro Word
print("\n" + "=" * 80)
print("8. PLACEHOLDER PRO WORD SABLONU:")
print("=" * 80)
print("{{ section_generated_texts.jedenacta_text_podminka }}")
print("\nALE pozor! V generate_word_from_two_sources.py se texty predavaji jako:")
print("context['section_generated_texts'] = texts")
print("\nTakze placeholder musi byt:")
print("{{ section_generated_texts.jedenacta_text_podminka }}")
