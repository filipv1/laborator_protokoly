"""
Test skript pro ověření funkčnosti paty_text_podminka (nadlimitní síly nad 70%)
"""
import json
import sys
from core.text_generator import _calculate_paty_text_podminka, generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_paty_text_real_data():
    """Test s reálnými daty z lsz_results.json"""
    print("=" * 80)
    print("TEST: paty_text_podminka s reálnými daty")
    print("=" * 80)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    # Zobraz data z řádku 21 (force_over_70)
    row21 = results_data["table_force_distribution"]["21"]

    print("Vstupní data z table_force_distribution řádek 21 (force_over_70):")
    print(f"  force_over_70_phk_extenzory: {row21.get('force_over_70_phk_extenzory')}")
    print(f"  force_over_70_phk_flexory: {row21.get('force_over_70_phk_flexory')}")
    print(f"  force_over_70_lhk_extenzory: {row21.get('force_over_70_lhk_extenzory')}")
    print(f"  force_over_70_lhk_flexory: {row21.get('force_over_70_lhk_flexory')}")
    print()

    # Konvertuj na flags
    values = [
        row21.get('force_over_70_phk_extenzory', 0),
        row21.get('force_over_70_phk_flexory', 0),
        row21.get('force_over_70_lhk_extenzory', 0),
        row21.get('force_over_70_lhk_flexory', 0)
    ]
    values = [v if v is not None else 0 for v in values]
    flags = tuple(1 if v >= 1 else 0 for v in values)

    print(f"Konverze na flags: {flags}")
    print()

    # Vygeneruj text
    result = _calculate_paty_text_podminka(results_data)
    print(f"VÝSLEDNÝ TEXT:")
    print(f"  {result}")
    print()

    print("=" * 80)
    print()


def test_all_16_combinations():
    """Test VŠECH 16 kombinací (2^4 = 16)"""
    print("=" * 80)
    print("TEST: Všech 16 kombinací páté podmínky")
    print("=" * 80)
    print()

    # Načti základní data
    with open("lsz_results.json", encoding="utf-8") as f:
        base_results = json.load(f)

    # Definice všech 16 kombinací a očekávaných výsledků
    test_cases = [
        ((0, 0, 0, 0), "nedochází"),

        ((0, 0, 0, 1), "flexorů LHK"),
        ((0, 0, 1, 0), "extenzorů LHK"),
        ((0, 0, 1, 1), "levé ruky a předloktí"),

        ((0, 1, 0, 0), "flexorů PHK"),
        ((0, 1, 0, 1), "flexorových svalových skupin"),
        ((0, 1, 1, 0), "flexorů PHK a extenzorů LHK"),
        ((0, 1, 1, 1), "flexorů PHK, extenzorů LHK a flexorů LHK"),

        ((1, 0, 0, 0), "extenzorů PHK"),
        ((1, 0, 0, 1), "extenzorů PHK a flexorů LHK"),
        ((1, 0, 1, 0), "extenzorových svalových skupin"),
        ((1, 0, 1, 1), "extenzorů PHK, extenzorů LHK a flexorů LHK"),

        ((1, 1, 0, 0), "pravé ruky a předloktí"),
        ((1, 1, 0, 1), "extenzorů PHK, flexorů PHK a flexorů LHK"),
        ((1, 1, 1, 0), "extenzorů PHK, flexorů PHK a extenzorů LHK"),
        ((1, 1, 1, 1), "extenzorů PHK, flexorů PHK, extenzorů LHK a flexorů LHK")
    ]

    passed = 0
    failed = 0

    for i, (pattern, expected_substring) in enumerate(test_cases, 1):
        print(f"TEST {i}/16: Pattern {pattern}")
        print("-" * 80)

        # Vytvoř testovací data
        results = base_results.copy()
        results["table_force_distribution"]["21"] = {
            "activity": "Celkem",
            "force_over_70_phk_extenzory": pattern[0],
            "force_over_70_phk_flexory": pattern[1],
            "force_over_70_lhk_extenzory": pattern[2],
            "force_over_70_lhk_flexory": pattern[3]
        }

        # Vygeneruj text
        result = _calculate_paty_text_podminka(results)

        # Ověř, že výsledek obsahuje očekávaný substring
        if expected_substring in result:
            print(f"✓ PASS: '{result}'")
            passed += 1
        else:
            print(f"✗ FAIL: Očekáváno '{expected_substring}' v textu")
            print(f"  Dostáno: '{result}'")
            failed += 1

        print()

    print("=" * 80)
    print(f"VÝSLEDEK: {passed}/16 testů prošlo, {failed}/16 selhalo")
    print("=" * 80)
    print()

    if failed == 0:
        print("✓ VŠECH 16 KOMBINACÍ FUNGUJE SPRÁVNĚ!")
    else:
        print(f"✗ NĚKTERÉ TESTY SELHALY ({failed} testů)")


def test_integration_all_five():
    """Test všech 5 podmínek dohromady"""
    print()
    print("=" * 80)
    print("INTEGRAČNÍ TEST: Všechny 5 podmínky")
    print("=" * 80)
    print()

    with open("measurement_data.json", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    # Vygeneruj všechny conditional texty
    conditional_texts = generate_conditional_texts(measurement_data, results_data)

    print("VYGENEROVANÉ CONDITIONAL TEXTY:")
    print("-" * 80)
    for i, (key, value) in enumerate(conditional_texts.items(), 1):
        print(f"{i}. {key}:")
        print(f"   {value}")
        print()

    # Ověř, že jsou všechny klíče
    expected_keys = [
        "prvni_text_podminka_pocetdni",
        "druhy_text_podminka_limit1",
        "treti_text_podminka_limit1",
        "ctvrty_text_podminka",
        "paty_text_podminka"
    ]

    all_present = True
    for key in expected_keys:
        if key not in conditional_texts:
            print(f"✗ Chybí klíč: {key}")
            all_present = False

    if all_present:
        print("=" * 80)
        print("✓ VŠECHNY 5 PODMÍNKY VYGENEROVÁNY ÚSPĚŠNĚ")
        print("=" * 80)
        print()
        print(f"Celkem vygenerováno: {len(conditional_texts)} conditional textů")


if __name__ == "__main__":
    test_paty_text_real_data()
    test_all_16_combinations()
    test_integration_all_five()
