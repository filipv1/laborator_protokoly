"""
Test všech 4 textových variant pro druhy_text_podminka_limit1
"""
import json
import sys
from core.text_generator import _calculate_druhy_text_podminka_limit1

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_all_variants():
    """Test všech 4 kombinací (extenzor_flag, flexor_flag)"""
    print("=" * 80)
    print("TEST: Všechny 4 textové varianty")
    print("=" * 80)
    print()

    # Načti reálnou tabulku
    with open("lsz_results.json", encoding="utf-8") as f:
        base_results = json.load(f)

    # Test case 1: (0, 0) - oba v limitu
    print("TEST 1: (0, 0) - oba V LIMITU")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Phk_Extenzor"] = 8
    results["Fmax_Phk_Flexor"] = 5.5
    results["phk_number_of_movements"] = 6000
    # Fmax=8 → limit 24300, Fmax=6 → limit ? (musí být > 6000)
    text = _calculate_druhy_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=8, Fmax_Flex=5.5, movements=6000")
    print(f"Text: {text}")
    print()

    # Test case 2: (1, 1) - oba překročené
    print("TEST 2: (1, 1) - oba PŘEKROČENÉ")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Phk_Extenzor"] = 50
    results["Fmax_Phk_Flexor"] = 50
    results["phk_number_of_movements"] = 100000
    # Fmax=50 → limit 2700, 100000 > 2700 → oba překročené
    text = _calculate_druhy_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=50, Fmax_Flex=50, movements=100000")
    print(f"Text: {text}")
    print()

    # Test case 3: (1, 0) - pouze extenzory překročené
    print("TEST 3: (1, 0) - pouze EXTENZORY překročené")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Phk_Extenzor"] = 50  # limit 2700
    results["Fmax_Phk_Flexor"] = 7     # limit 27600
    results["phk_number_of_movements"] = 15000
    # 15000 > 2700 (ext překročen), 15000 < 27600 (flex OK)
    text = _calculate_druhy_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=50, Fmax_Flex=7, movements=15000")
    print(f"Text: {text}")
    print()

    # Test case 4: (0, 1) - pouze flexory překročené
    print("TEST 4: (0, 1) - pouze FLEXORY překročené")
    print("-" * 80)
    results = base_results.copy()
    results["Fmax_Phk_Extenzor"] = 7   # limit 27600
    results["Fmax_Phk_Flexor"] = 50    # limit 2700
    results["phk_number_of_movements"] = 15000
    # 15000 < 27600 (ext OK), 15000 > 2700 (flex překročen)
    text = _calculate_druhy_text_podminka_limit1(results)
    print(f"Vstup: Fmax_Ext=7, Fmax_Flex=50, movements=15000")
    print(f"Text: {text}")
    print()

    print("=" * 80)
    print("✓ VŠECHNY VARIANTY OTESTOVÁNY")
    print("=" * 80)


if __name__ == "__main__":
    test_all_variants()
