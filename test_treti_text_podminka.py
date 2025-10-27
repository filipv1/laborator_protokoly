"""
Test skript pro ověření funkčnosti treti_text_podminka_limit1 (LHK)
"""
import json
import sys
from core.text_generator import generate_conditional_texts, _calculate_treti_text_podminka_limit1

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_treti_text_podminka():
    """Test hlavní logiky pro třetí podmínku (LHK)"""
    print("=" * 80)
    print("TEST: treti_text_podminka_limit1 s reálnými daty")
    print("=" * 80)

    # Načti reálná data
    with open("measurement_data.json", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    # Zobraz vstupní data
    print("Vstupní data (LHK):")
    print(f"  Fmax_Lhk_Extenzor: {results_data['Fmax_Lhk_Extenzor']}")
    print(f"  Fmax_Lhk_Flexor: {results_data['Fmax_Lhk_Flexor']}")
    print(f"  lhk_number_of_movements: {results_data['lhk_number_of_movements']}")
    print()

    # Zaokrouhli
    from core.text_generator import _math_round
    fmax_ext_rounded = _math_round(results_data['Fmax_Lhk_Extenzor'])
    fmax_flex_rounded = _math_round(results_data['Fmax_Lhk_Flexor'])

    print(f"Zaokrouhlené hodnoty:")
    print(f"  Fmax_Lhk_Extenzor: {results_data['Fmax_Lhk_Extenzor']} → {fmax_ext_rounded}")
    print(f"  Fmax_Lhk_Flexor: {results_data['Fmax_Lhk_Flexor']} → {fmax_flex_rounded}")
    print()

    # Najdi limity
    from core.text_generator import _find_in_table_W4_Y51
    table = results_data["table_W4_Y51"]
    row_ext = _find_in_table_W4_Y51(table, fmax_ext_rounded)
    row_flex = _find_in_table_W4_Y51(table, fmax_flex_rounded)

    print(f"Limity z tabulky:")
    if row_ext:
        print(f"  Extenzory (Fmax={fmax_ext_rounded}): limit LHK = {row_ext['lhk']}")
    if row_flex:
        print(f"  Flexory (Fmax={fmax_flex_rounded}): limit LHK = {row_flex['lhk']}")
    print()

    # Porovnání
    lhk_movements = results_data['lhk_number_of_movements']
    print(f"Porovnání s naměřeným počtem pohybů ({lhk_movements}):")
    if row_ext:
        ext_flag = 1 if lhk_movements > row_ext['lhk'] else 0
        print(f"  Extenzory: {lhk_movements} > {row_ext['lhk']} ? → flag = {ext_flag}")
    if row_flex:
        flex_flag = 1 if lhk_movements > row_flex['lhk'] else 0
        print(f"  Flexory: {lhk_movements} > {row_flex['lhk']} ? → flag = {flex_flag}")
    print()

    # Vygeneruj text
    conditional_texts = generate_conditional_texts(measurement_data, results_data)

    print("=" * 80)
    print("VYGENEROVANÉ TEXTY:")
    print("=" * 80)
    for key, value in conditional_texts.items():
        print(f"\n{key}:")
        print(f"  {value}")

    print()
    print("=" * 80)
    print("✓ TEST DOKONČEN")
    print("=" * 80)


def test_lhk_all_variants():
    """Test všech 4 kombinací pro LHK"""
    print()
    print("=" * 80)
    print("TEST: Všechny 4 textové varianty pro LHK")
    print("=" * 80)
    print()

    # Načti reálnou tabulku
    with open("lsz_results.json", encoding="utf-8") as f:
        base_results = json.load(f)

    # Test case 1: (0, 0) - oba v limitu
    print("TEST 1: (0, 0) - oba V LIMITU")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Lhk_Extenzor"] = 8
    results["Fmax_Lhk_Flexor"] = 5.5
    results["lhk_number_of_movements"] = 6000
    text = _calculate_treti_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=8, Fmax_Flex=5.5, movements=6000")
    print(f"Text: {text}")
    print()

    # Test case 2: (1, 1) - oba překročené
    print("TEST 2: (1, 1) - oba PŘEKROČENÉ")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Lhk_Extenzor"] = 50
    results["Fmax_Lhk_Flexor"] = 50
    results["lhk_number_of_movements"] = 100000
    text = _calculate_treti_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=50, Fmax_Flex=50, movements=100000")
    print(f"Text: {text}")
    print()

    # Test case 3: (1, 0) - pouze extenzory překročené
    print("TEST 3: (1, 0) - pouze EXTENZORY překročené")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Lhk_Extenzor"] = 50
    results["Fmax_Lhk_Flexor"] = 7
    results["lhk_number_of_movements"] = 15000
    text = _calculate_treti_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=50, Fmax_Flex=7, movements=15000")
    print(f"Text: {text}")
    print()

    # Test case 4: (0, 1) - pouze flexory překročené
    print("TEST 4: (0, 1) - pouze FLEXORY překročené")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Lhk_Extenzor"] = 7
    results["Fmax_Lhk_Flexor"] = 50
    results["lhk_number_of_movements"] = 15000
    text = _calculate_treti_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=7, Fmax_Flex=50, movements=15000")
    print(f"Text: {text}")
    print()

    print("=" * 80)
    print("✓ VŠECHNY LHK VARIANTY OTESTOVÁNY")
    print("=" * 80)


if __name__ == "__main__":
    test_treti_text_podminka()
    test_lhk_all_variants()
