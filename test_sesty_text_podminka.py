"""
Test skript pro ověření funkčnosti sesty_text_podminka (hodnoty > 100)
"""
import json
import sys
from core.text_generator import _calculate_sesty_text_podminka, generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_sesty_text_real_data():
    """Test s reálnými daty z lsz_results.json"""
    print("=" * 80)
    print("TEST: sesty_text_podminka s reálnými daty")
    print("=" * 80)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    # Zobraz data z řádku 21 (všech 8 hodnot)
    row21 = results_data["table_force_distribution"]["21"]

    print("Vstupní data z table_force_distribution řádek 21 (všech 8 hodnot):")
    print(f"  force_55_70_phk_extenzory: {row21.get('force_55_70_phk_extenzory')}")
    print(f"  force_55_70_phk_flexory: {row21.get('force_55_70_phk_flexory')}")
    print(f"  force_55_70_lhk_extenzory: {row21.get('force_55_70_lhk_extenzory')}")
    print(f"  force_55_70_lhk_flexory: {row21.get('force_55_70_lhk_flexory')}")
    print(f"  force_over_70_phk_extenzory: {row21.get('force_over_70_phk_extenzory')}")
    print(f"  force_over_70_phk_flexory: {row21.get('force_over_70_phk_flexory')}")
    print(f"  force_over_70_lhk_extenzory: {row21.get('force_over_70_lhk_extenzory')}")
    print(f"  force_over_70_lhk_flexory: {row21.get('force_over_70_lhk_flexory')}")
    print()

    # Zjisti, zda je nějaká hodnota > 100
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

    any_over_100 = any(v > 100 for v in values)
    max_value = max(values)

    print(f"Analýza:")
    print(f"  Maximální hodnota: {max_value}")
    print(f"  Je nějaká hodnota > 100: {any_over_100}")
    print()

    # Vygeneruj text
    result = _calculate_sesty_text_podminka(results_data)
    print(f"VÝSLEDNÝ TEXT: '{result}'")
    print()

    print("=" * 80)
    print()


def test_both_variants():
    """Test obou variant (je / není)"""
    print("=" * 80)
    print("TEST: Obě varianty šesté podmínky")
    print("=" * 80)
    print()

    # Načti základní data
    with open("lsz_results.json", encoding="utf-8") as f:
        base_results = json.load(f)

    # VARIANTA 1: Všechny hodnoty <= 100 → "není"
    print("VARIANTA 1: Všechny hodnoty <= 100")
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
    result = _calculate_sesty_text_podminka(results)
    print(f"Max hodnota: 45")
    print(f"Výsledek: '{result}'")
    assert result == "není", f"Očekáváno 'není', ale je '{result}'"
    print("✓ Správně")
    print()

    # VARIANTA 2: Alespoň jedna hodnota > 100 → "je"
    print("VARIANTA 2: Alespoň jedna hodnota > 100")
    print("-" * 80)
    results = base_results.copy()
    results["table_force_distribution"]["21"] = {
        "activity": "Celkem",
        "force_55_70_phk_extenzory": 1,
        "force_55_70_phk_flexory": 3,
        "force_55_70_lhk_extenzory": 150,  # > 100
        "force_55_70_lhk_flexory": 2,
        "force_over_70_phk_extenzory": 0,
        "force_over_70_phk_flexory": 0,
        "force_over_70_lhk_extenzory": 0,
        "force_over_70_lhk_flexory": 0
    }
    result = _calculate_sesty_text_podminka(results)
    print(f"Max hodnota: 150")
    print(f"Výsledek: '{result}'")
    assert result == "je", f"Očekáváno 'je', ale je '{result}'"
    print("✓ Správně")
    print()

    # VARIANTA 3: Více hodnot > 100 → "je"
    print("VARIANTA 3: Více hodnot > 100")
    print("-" * 80)
    results = base_results.copy()
    results["table_force_distribution"]["21"] = {
        "activity": "Celkem",
        "force_55_70_phk_extenzory": 200,  # > 100
        "force_55_70_phk_flexory": 300,  # > 100
        "force_55_70_lhk_extenzory": 150,  # > 100
        "force_55_70_lhk_flexory": 2,
        "force_over_70_phk_extenzory": 0,
        "force_over_70_phk_flexory": 0,
        "force_over_70_lhk_extenzory": 0,
        "force_over_70_lhk_flexory": 0
    }
    result = _calculate_sesty_text_podminka(results)
    print(f"Max hodnota: 300")
    print(f"Výsledek: '{result}'")
    assert result == "je", f"Očekáváno 'je', ale je '{result}'"
    print("✓ Správně")
    print()

    # VARIANTA 4: Přesně 100 → "není" (není VĚTŠÍ než 100)
    print("VARIANTA 4: Přesně hodnota = 100 (není větší)")
    print("-" * 80)
    results = base_results.copy()
    results["table_force_distribution"]["21"] = {
        "activity": "Celkem",
        "force_55_70_phk_extenzory": 100,  # = 100 (ne > 100)
        "force_55_70_phk_flexory": 3,
        "force_55_70_lhk_extenzory": 45,
        "force_55_70_lhk_flexory": 2,
        "force_over_70_phk_extenzory": 0,
        "force_over_70_phk_flexory": 0,
        "force_over_70_lhk_extenzory": 0,
        "force_over_70_lhk_flexory": 0
    }
    result = _calculate_sesty_text_podminka(results)
    print(f"Max hodnota: 100")
    print(f"Výsledek: '{result}'")
    assert result == "není", f"Očekáváno 'není', ale je '{result}'"
    print("✓ Správně")
    print()

    print("=" * 80)
    print("✓ OBĚ VARIANTY FUNGUJÍ SPRÁVNĚ")
    print("=" * 80)
    print()


def test_integration_all_six():
    """Test všech 6 podmínek dohromady"""
    print()
    print("=" * 80)
    print("INTEGRAČNÍ TEST: Všechny 6 podmínky")
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
        "paty_text_podminka",
        "sesty_text_podminka"
    ]

    all_present = True
    for key in expected_keys:
        if key not in conditional_texts:
            print(f"✗ Chybí klíč: {key}")
            all_present = False

    if all_present:
        print("=" * 80)
        print("✓ VŠECHNY 6 PODMÍNKY VYGENEROVÁNY ÚSPĚŠNĚ")
        print("=" * 80)
        print()
        print(f"Celkem vygenerováno: {len(conditional_texts)} conditional textů")


if __name__ == "__main__":
    test_sesty_text_real_data()
    test_both_variants()
    test_integration_all_six()
