"""
Test skript pro ověření funkčnosti ctvrty_text_podminka (force_distribution)
"""
import json
import sys
from core.text_generator import _calculate_ctvrty_text_podminka, generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_ctvrty_text_real_data():
    """Test s reálnými daty z lsz_results.json"""
    print("=" * 80)
    print("TEST: ctvrty_text_podminka s reálnými daty")
    print("=" * 80)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    # Zobraz data z řádku 21
    row21 = results_data["table_force_distribution"]["21"]

    print("Vstupní data z table_force_distribution řádek 21 (Celkem):")
    print(f"  force_55_70_phk_extenzory: {row21.get('force_55_70_phk_extenzory')}")
    print(f"  force_55_70_phk_flexory: {row21.get('force_55_70_phk_flexory')}")
    print(f"  force_55_70_lhk_extenzory: {row21.get('force_55_70_lhk_extenzory')}")
    print(f"  force_55_70_lhk_flexory: {row21.get('force_55_70_lhk_flexory')}")
    print(f"  force_over_70_phk_extenzory: {row21.get('force_over_70_phk_extenzory')}")
    print(f"  force_over_70_phk_flexory: {row21.get('force_over_70_phk_flexory')}")
    print(f"  force_over_70_lhk_extenzory: {row21.get('force_over_70_lhk_extenzory')}")
    print(f"  force_over_70_lhk_flexory: {row21.get('force_over_70_lhk_flexory')}")
    print()

    # Vygeneruj text
    result = _calculate_ctvrty_text_podminka(results_data)
    print(f"VÝSLEDNÝ TEXT: '{result}'")
    print()

    # Analýza
    values = [
        row21.get('force_55_70_phk_extenzory', 0),
        row21.get('force_55_70_phk_flexory', 0),
        row21.get('force_55_70_lhk_extenzory', 0),
        row21.get('force_55_70_lhk_flexory', 0),
        row21.get('force_over_70_phk_extenzory', 0),
        row21.get('force_over_70_phk_flexory', 0),
        row21.get('force_over_70_lhk_extenzory', 0),
        row21.get('force_over_70_lhk_flexory', 0)
    ]
    values = [v if v is not None else 0 for v in values]

    all_zero = all(v == 0 for v in values)
    all_one_plus = all(v >= 1 for v in values)

    print("Analýza:")
    print(f"  Všechny hodnoty == 0: {all_zero}")
    print(f"  Všechny hodnoty >= 1: {all_one_plus}")
    print(f"  Některé >= 1, některé == 0: {not all_zero and not all_one_plus}")
    print()
    print("=" * 80)
    print()


def test_all_three_variants():
    """Test všech 3 variant (nejsou, ojediněle, pravidelně)"""
    print("=" * 80)
    print("TEST: Všechny 3 varianty textu")
    print("=" * 80)
    print()

    # Načti základní data
    with open("lsz_results.json", encoding="utf-8") as f:
        base_results = json.load(f)

    # VARIANTA 1: Všechny == 0 → "nejsou"
    print("VARIANTA 1: Všechny hodnoty == 0")
    print("-" * 80)
    results = base_results.copy()
    results["table_force_distribution"]["21"] = {
        "activity": "Celkem",
        "force_55_70_phk_extenzory": 0,
        "force_55_70_phk_flexory": 0,
        "force_55_70_lhk_extenzory": 0,
        "force_55_70_lhk_flexory": 0,
        "force_over_70_phk_extenzory": 0,
        "force_over_70_phk_flexory": 0,
        "force_over_70_lhk_extenzory": 0,
        "force_over_70_lhk_flexory": 0
    }
    result = _calculate_ctvrty_text_podminka(results)
    print(f"Výsledek: '{result}'")
    assert result == "nejsou", f"Očekáváno 'nejsou', ale je '{result}'"
    print("✓ Správně")
    print()

    # VARIANTA 2: Některé >= 1 → "ojediněle"
    print("VARIANTA 2: Některé hodnoty >= 1, některé == 0")
    print("-" * 80)
    results = base_results.copy()
    results["table_force_distribution"]["21"] = {
        "activity": "Celkem",
        "force_55_70_phk_extenzory": 1,
        "force_55_70_phk_flexory": 3,
        "force_55_70_lhk_extenzory": 45,
        "force_55_70_lhk_flexory": 2,
        "force_over_70_phk_extenzory": 0,
        "force_over_70_phk_flexory": 0,
        "force_over_70_lhk_extenzory": 0,
        "force_over_70_lhk_flexory": 0
    }
    result = _calculate_ctvrty_text_podminka(results)
    print(f"Výsledek: '{result}'")
    assert result == "ojediněle", f"Očekáváno 'ojediněle', ale je '{result}'"
    print("✓ Správně")
    print()

    # VARIANTA 3: Všechny >= 1 → "pravidelně"
    print("VARIANTA 3: Všechny hodnoty >= 1")
    print("-" * 80)
    results = base_results.copy()
    results["table_force_distribution"]["21"] = {
        "activity": "Celkem",
        "force_55_70_phk_extenzory": 5,
        "force_55_70_phk_flexory": 3,
        "force_55_70_lhk_extenzory": 45,
        "force_55_70_lhk_flexory": 2,
        "force_over_70_phk_extenzory": 1,
        "force_over_70_phk_flexory": 1,
        "force_over_70_lhk_extenzory": 1,
        "force_over_70_lhk_flexory": 1
    }
    result = _calculate_ctvrty_text_podminka(results)
    print(f"Výsledek: '{result}'")
    assert result == "pravidelně", f"Očekáváno 'pravidelně', ale je '{result}'"
    print("✓ Správně")
    print()

    print("=" * 80)
    print("✓ VŠECHNY 3 VARIANTY FUNGUJÍ SPRÁVNĚ")
    print("=" * 80)
    print()


def test_integration_all_four():
    """Test všech 4 podmínek dohromady"""
    print("=" * 80)
    print("INTEGRAČNÍ TEST: Všechny 4 podmínky")
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

    # Ověř, že jsou všechny 4 klíče
    expected_keys = [
        "prvni_text_podminka_pocetdni",
        "druhy_text_podminka_limit1",
        "treti_text_podminka_limit1",
        "ctvrty_text_podminka"
    ]

    for key in expected_keys:
        assert key in conditional_texts, f"Chybí klíč: {key}"

    print("=" * 80)
    print("✓ VŠECHNY 4 PODMÍNKY VYGENEROVÁNY ÚSPĚŠNĚ")
    print("=" * 80)


if __name__ == "__main__":
    test_ctvrty_text_real_data()
    test_all_three_variants()
    test_integration_all_four()
