"""
Test skript pro ověření funkčnosti druhy_text_podminka_limit1
"""
import json
import sys
from core.text_generator import generate_conditional_texts, _math_round, _find_in_table_W4_Y51

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_math_round():
    """Test matematického zaokrouhlování"""
    print("=" * 80)
    print("TEST: Matematické zaokrouhlování")
    print("=" * 80)

    test_cases = [
        (9.5, 10),
        (8.5, 9),
        (7.4, 7),
        (7.6, 8),
        (5.5, 6),
    ]

    for value, expected in test_cases:
        result = _math_round(value)
        status = "✓" if result == expected else "✗"
        print(f"{status} _math_round({value}) = {result} (očekáváno: {expected})")

    print()


def test_table_lookup():
    """Test vyhledávání v tabulce"""
    print("=" * 80)
    print("TEST: Vyhledávání v table_W4_Y51")
    print("=" * 80)

    # Načti reálnou tabulku
    with open("lsz_results.json", encoding="utf-8") as f:
        results = json.load(f)

    table = results["table_W4_Y51"]

    # Test case 1: Fmax = 8 (existuje v tabulce)
    row = _find_in_table_W4_Y51(table, 8)
    print(f"Hledám Fmax = 8:")
    if row:
        print(f"  ✓ Nalezeno: fmax={row['fmax']}, phk={row['phk']}, lhk={row['lhk']}")
    else:
        print(f"  ✗ Nenalezeno")

    # Test case 2: Fmax = 10 (existuje v tabulce)
    row = _find_in_table_W4_Y51(table, 10)
    print(f"Hledám Fmax = 10:")
    if row:
        print(f"  ✓ Nalezeno: fmax={row['fmax']}, phk={row['phk']}, lhk={row['lhk']}")
    else:
        print(f"  ✗ Nenalezeno")

    # Test case 3: Fmax = 100 (neexistuje v tabulce)
    row = _find_in_table_W4_Y51(table, 100)
    print(f"Hledám Fmax = 100:")
    if row:
        print(f"  ✗ Nalezeno (nečekáno)")
    else:
        print(f"  ✓ Nenalezeno (správně)")

    print()


def test_druhy_text_podminka():
    """Test hlavní logiky pro druhou podmínku"""
    print("=" * 80)
    print("TEST: druhy_text_podminka_limit1 s reálnými daty")
    print("=" * 80)

    # Načti reálná data
    with open("measurement_data.json", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    # Zobraz vstupní data
    print("Vstupní data:")
    print(f"  Fmax_Phk_Extenzor: {results_data['Fmax_Phk_Extenzor']}")
    print(f"  Fmax_Phk_Flexor: {results_data['Fmax_Phk_Flexor']}")
    print(f"  phk_number_of_movements: {results_data['phk_number_of_movements']}")
    print()

    # Zaokrouhli
    from core.text_generator import _math_round
    fmax_ext_rounded = _math_round(results_data['Fmax_Phk_Extenzor'])
    fmax_flex_rounded = _math_round(results_data['Fmax_Phk_Flexor'])

    print(f"Zaokrouhlené hodnoty:")
    print(f"  Fmax_Phk_Extenzor: {results_data['Fmax_Phk_Extenzor']} → {fmax_ext_rounded}")
    print(f"  Fmax_Phk_Flexor: {results_data['Fmax_Phk_Flexor']} → {fmax_flex_rounded}")
    print()

    # Najdi limity
    from core.text_generator import _find_in_table_W4_Y51
    table = results_data["table_W4_Y51"]
    row_ext = _find_in_table_W4_Y51(table, fmax_ext_rounded)
    row_flex = _find_in_table_W4_Y51(table, fmax_flex_rounded)

    print(f"Limity z tabulky:")
    if row_ext:
        print(f"  Extenzory (Fmax={fmax_ext_rounded}): limit PHK = {row_ext['phk']}")
    if row_flex:
        print(f"  Flexory (Fmax={fmax_flex_rounded}): limit PHK = {row_flex['phk']}")
    print()

    # Porovnání
    phk_movements = results_data['phk_number_of_movements']
    print(f"Porovnání s naměřeným počtem pohybů ({phk_movements}):")
    if row_ext:
        ext_flag = 1 if phk_movements > row_ext['phk'] else 0
        print(f"  Extenzory: {phk_movements} > {row_ext['phk']} ? → flag = {ext_flag}")
    if row_flex:
        flex_flag = 1 if phk_movements > row_flex['phk'] else 0
        print(f"  Flexory: {phk_movements} > {row_flex['phk']} ? → flag = {flex_flag}")
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


if __name__ == "__main__":
    test_math_round()
    test_table_lookup()
    test_druhy_text_podminka()
