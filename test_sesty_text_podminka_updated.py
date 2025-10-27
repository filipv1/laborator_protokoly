"""
Test pro sesty_text_podminka - UPDATED VERSION
Nyní bere v úvahu POUZE force_over_70_* hodnoty (ne force_55_70_*)

Podmínka:
- Pokud jakákoliv z 4 hodnot force_over_70_* > 100 → "je"
- Jinak → "není"
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from core.text_generator import _calculate_sesty_text_podminka


def test_sesty_text_podminka_updated():
    """Test šesté podmínky s novou logikou (pouze force_over_70)"""

    print("=" * 80)
    print("TEST: sesty_text_podminka - UPDATED (pouze force_over_70)")
    print("=" * 80)

    # TEST 1: Všechny force_over_70 hodnoty < 100 → "není"
    print("\n[TEST 1] Všechny force_over_70 < 100 → není")
    results_data_1 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 150,  # > 100 ale IGNORUJE SE
                "force_55_70_phk_flexory": 120,    # > 100 ale IGNORUJE SE
                "force_55_70_lhk_extenzory": 110,  # > 100 ale IGNORUJE SE
                "force_55_70_lhk_flexory": 130,    # > 100 ale IGNORUJE SE
                "force_over_70_phk_extenzory": 50,  # < 100 ✓
                "force_over_70_phk_flexory": 30,    # < 100 ✓
                "force_over_70_lhk_extenzory": 40,  # < 100 ✓
                "force_over_70_lhk_flexory": 25     # < 100 ✓
            }
        }
    }
    result_1 = _calculate_sesty_text_podminka(results_data_1)
    print(f"   force_55_70: 150, 120, 110, 130 (všechny > 100, ale IGNORUJÍ SE)")
    print(f"   force_over_70: 50, 30, 40, 25 (všechny < 100)")
    print(f"   Výsledek: '{result_1}'")
    assert result_1 == "není", f"Expected 'není', got '{result_1}'"
    print("   ✓ PASS - Správně ignoruje force_55_70 hodnoty")

    # TEST 2: Jedna force_over_70 hodnota > 100 → "je"
    print("\n[TEST 2] Jedna force_over_70 > 100 → je")
    results_data_2 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 10,
                "force_55_70_phk_flexory": 20,
                "force_55_70_lhk_extenzory": 15,
                "force_55_70_lhk_flexory": 25,
                "force_over_70_phk_extenzory": 150,  # > 100 ✓
                "force_over_70_phk_flexory": 30,
                "force_over_70_lhk_extenzory": 40,
                "force_over_70_lhk_flexory": 25
            }
        }
    }
    result_2 = _calculate_sesty_text_podminka(results_data_2)
    print(f"   force_over_70_phk_extenzory: 150 > 100")
    print(f"   Výsledek: '{result_2}'")
    assert result_2 == "je", f"Expected 'je', got '{result_2}'"
    print("   ✓ PASS")

    # TEST 3: Všechny force_over_70 hodnoty > 100 → "je"
    print("\n[TEST 3] Všechny force_over_70 > 100 → je")
    results_data_3 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 10,
                "force_55_70_phk_flexory": 20,
                "force_55_70_lhk_extenzory": 15,
                "force_55_70_lhk_flexory": 25,
                "force_over_70_phk_extenzory": 150,
                "force_over_70_phk_flexory": 120,
                "force_over_70_lhk_extenzory": 130,
                "force_over_70_lhk_flexory": 110
            }
        }
    }
    result_3 = _calculate_sesty_text_podminka(results_data_3)
    print(f"   force_over_70: 150, 120, 130, 110 (všechny > 100)")
    print(f"   Výsledek: '{result_3}'")
    assert result_3 == "je", f"Expected 'je', got '{result_3}'"
    print("   ✓ PASS")

    # TEST 4: Hraničný případ - force_over_70 = 100 → "není"
    print("\n[TEST 4] Hraničný: force_over_70 = 100 → není")
    results_data_4 = {
        "table_force_distribution": {
            "21": {
                "force_over_70_phk_extenzory": 100,
                "force_over_70_phk_flexory": 100,
                "force_over_70_lhk_extenzory": 100,
                "force_over_70_lhk_flexory": 100
            }
        }
    }
    result_4 = _calculate_sesty_text_podminka(results_data_4)
    print(f"   Všechny force_over_70 = 100 (ne větší)")
    print(f"   Výsledek: '{result_4}'")
    assert result_4 == "není", f"Expected 'není', got '{result_4}'"
    print("   ✓ PASS")

    # TEST 5: Hraničný případ - force_over_70 = 101 → "je"
    print("\n[TEST 5] Hraničný: force_over_70 = 101 → je")
    results_data_5 = {
        "table_force_distribution": {
            "21": {
                "force_over_70_phk_extenzory": 101,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            }
        }
    }
    result_5 = _calculate_sesty_text_podminka(results_data_5)
    print(f"   force_over_70_phk_extenzory = 101 > 100")
    print(f"   Výsledek: '{result_5}'")
    assert result_5 == "je", f"Expected 'je', got '{result_5}'"
    print("   ✓ PASS")

    # TEST 6: Všechny force_over_70 = 0 → "není"
    print("\n[TEST 6] Všechny force_over_70 = 0 → není")
    results_data_6 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 200,  # Ignoruje se
                "force_55_70_phk_flexory": 200,    # Ignoruje se
                "force_55_70_lhk_extenzory": 200,  # Ignoruje se
                "force_55_70_lhk_flexory": 200,    # Ignoruje se
                "force_over_70_phk_extenzory": 0,
                "force_over_70_phk_flexory": 0,
                "force_over_70_lhk_extenzory": 0,
                "force_over_70_lhk_flexory": 0
            }
        }
    }
    result_6 = _calculate_sesty_text_podminka(results_data_6)
    print(f"   force_55_70: všechny 200 (ignorují se)")
    print(f"   force_over_70: všechny 0")
    print(f"   Výsledek: '{result_6}'")
    assert result_6 == "není", f"Expected 'není', got '{result_6}'"
    print("   ✓ PASS - Správně ignoruje vysoké force_55_70 hodnoty")

    # TEST 7: Chybějící řádek 21 → fallback "není"
    print("\n[TEST 7] Chybějící řádek 21 → fallback 'není'")
    results_data_7 = {
        "table_force_distribution": {}
    }
    result_7 = _calculate_sesty_text_podminka(results_data_7)
    print(f"   Řádek 21 chybí → Výsledek: '{result_7}'")
    assert result_7 == "není", f"Expected 'není', got '{result_7}'"
    print("   ✓ PASS")

    # TEST 8: Mix - pouze force_over_70 se počítá
    print("\n[TEST 8] Kritický test: force_55_70=200, force_over_70=99 → není")
    results_data_8 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 200,  # > 100 ale IGNORUJE SE
                "force_55_70_phk_flexory": 200,    # > 100 ale IGNORUJE SE
                "force_55_70_lhk_extenzory": 200,  # > 100 ale IGNORUJE SE
                "force_55_70_lhk_flexory": 200,    # > 100 ale IGNORUJE SE
                "force_over_70_phk_extenzory": 99,  # < 100
                "force_over_70_phk_flexory": 99,    # < 100
                "force_over_70_lhk_extenzory": 99,  # < 100
                "force_over_70_lhk_flexory": 99     # < 100
            }
        }
    }
    result_8 = _calculate_sesty_text_podminka(results_data_8)
    print(f"   force_55_70: všechny 200 > 100 (ale IGNORUJÍ SE!)")
    print(f"   force_over_70: všechny 99 < 100")
    print(f"   Výsledek: '{result_8}'")
    assert result_8 == "není", f"Expected 'není', got '{result_8}'"
    print("   ✓ PASS - DŮLEŽITÉ: Potvrzeno že force_55_70 se ignorují!")

    print("\n" + "=" * 80)
    print("✅ VŠECHNY TESTY PROŠLY!")
    print("🎯 POTVRZENO: Šestá podmínka nyní bere v úvahu POUZE force_over_70 hodnoty")
    print("=" * 80)


if __name__ == "__main__":
    test_sesty_text_podminka_updated()
