"""
Test pro sedmy_text_podminka - prekroceni limitu pro velke svalove sily (55-70% Fmax)
UPDATED: Nyní vrací celé věty místo jednoslovných hodnot

Logika:
- limit = (work_duration / 2) + 360
- suma = soucet 4 hodnot force_55_70_* z radku 21
- pokud suma > limit -> celá věta o překročení
- pokud suma <= limit -> celá věta o nepřekročení
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from core.text_generator import _calculate_sedmy_text_podminka


def test_sedmy_text_podminka():
    """Testuje všechny scénáře sedmé podmínky"""

    print("=" * 80)
    print("TEST: sedmy_text_podminka - Překročení limitu velkých sil (55-70% Fmax)")
    print("=" * 80)

    EXPECTED_NEPREKRACUJE = "nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."
    EXPECTED_PREKRACUJE = "překračuje u měřených svalových skupin rukou a předloktí daný hygienický limit."

    # TEST 1: 480 min směna (8h), nízký součet → nepřekračuje
    print("\n[TEST 1] 480 min směna, součet=18, limit=600 → nepřekračuje")
    measurement_data_1 = {
        "section4_worker_a": {
            "work_duration": 480
        }
    }
    results_data_1 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 4,
                "force_55_70_phk_flexory": 4,
                "force_55_70_lhk_extenzory": 5,
                "force_55_70_lhk_flexory": 5
            }
        }
    }
    result_1 = _calculate_sedmy_text_podminka(measurement_data_1, results_data_1)
    print(f"   Součet: 4+4+5+5 = 18")
    print(f"   Limit: (480/2)+360 = 600")
    print(f"   18 ≤ 600 → Výsledek:")
    print(f"   '{result_1}'")
    assert result_1 == EXPECTED_NEPREKRACUJE, f"Expected '{EXPECTED_NEPREKRACUJE}', got '{result_1}'"
    print("   ✓ PASS")

    # TEST 2: 480 min směna, vysoký součet → překračuje
    print("\n[TEST 2] 480 min směna, součet=650, limit=600 → překračuje")
    measurement_data_2 = {
        "section4_worker_a": {
            "work_duration": 480
        }
    }
    results_data_2 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 200,
                "force_55_70_phk_flexory": 150,
                "force_55_70_lhk_extenzory": 150,
                "force_55_70_lhk_flexory": 150
            }
        }
    }
    result_2 = _calculate_sedmy_text_podminka(measurement_data_2, results_data_2)
    print(f"   Součet: 200+150+150+150 = 650")
    print(f"   Limit: (480/2)+360 = 600")
    print(f"   650 > 600 → Výsledek:")
    print(f"   '{result_2}'")
    assert result_2 == EXPECTED_PREKRACUJE, f"Expected '{EXPECTED_PREKRACUJE}', got '{result_2}'"
    print("   ✓ PASS")

    # TEST 3: 450 min směna (7.5h), součet=20, limit=585 → nepřekračuje
    print("\n[TEST 3] 450 min směna, součet=20, limit=585 → nepřekračuje")
    measurement_data_3 = {
        "section4_worker_a": {
            "work_duration": 450
        }
    }
    results_data_3 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 5,
                "force_55_70_phk_flexory": 5,
                "force_55_70_lhk_extenzory": 5,
                "force_55_70_lhk_flexory": 5
            }
        }
    }
    result_3 = _calculate_sedmy_text_podminka(measurement_data_3, results_data_3)
    print(f"   Součet: 5+5+5+5 = 20")
    print(f"   Limit: (450/2)+360 = 585")
    print(f"   20 ≤ 585 → Výsledek:")
    print(f"   '{result_3}'")
    assert result_3 == EXPECTED_NEPREKRACUJE, f"Expected '{EXPECTED_NEPREKRACUJE}', got '{result_3}'"
    print("   ✓ PASS")

    # TEST 4: 450 min směna, součet=600, limit=585 → překračuje
    print("\n[TEST 4] 450 min směna, součet=600, limit=585 → překračuje")
    measurement_data_4 = {
        "section4_worker_a": {
            "work_duration": 450
        }
    }
    results_data_4 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 150,
                "force_55_70_phk_flexory": 150,
                "force_55_70_lhk_extenzory": 150,
                "force_55_70_lhk_flexory": 150
            }
        }
    }
    result_4 = _calculate_sedmy_text_podminka(measurement_data_4, results_data_4)
    print(f"   Součet: 150+150+150+150 = 600")
    print(f"   Limit: (450/2)+360 = 585")
    print(f"   600 > 585 → Výsledek:")
    print(f"   '{result_4}'")
    assert result_4 == EXPECTED_PREKRACUJE, f"Expected '{EXPECTED_PREKRACUJE}', got '{result_4}'"
    print("   ✓ PASS")

    # TEST 5: 720 min směna (12h), součet=750, limit=720 → překračuje
    print("\n[TEST 5] 720 min směna, součet=750, limit=720 → překračuje")
    measurement_data_5 = {
        "section4_worker_a": {
            "work_duration": 720
        }
    }
    results_data_5 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 200,
                "force_55_70_phk_flexory": 200,
                "force_55_70_lhk_extenzory": 175,
                "force_55_70_lhk_flexory": 175
            }
        }
    }
    result_5 = _calculate_sedmy_text_podminka(measurement_data_5, results_data_5)
    print(f"   Součet: 200+200+175+175 = 750")
    print(f"   Limit: (720/2)+360 = 720")
    print(f"   750 > 720 → Výsledek:")
    print(f"   '{result_5}'")
    assert result_5 == EXPECTED_PREKRACUJE, f"Expected '{EXPECTED_PREKRACUJE}', got '{result_5}'"
    print("   ✓ PASS")

    # TEST 6: Hraničný případ - suma PRÁVĚ ROVNA limitu → nepřekračuje
    print("\n[TEST 6] Hraničný případ: suma=600, limit=600 → nepřekračuje")
    measurement_data_6 = {
        "section4_worker_a": {
            "work_duration": 480
        }
    }
    results_data_6 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 150,
                "force_55_70_phk_flexory": 150,
                "force_55_70_lhk_extenzory": 150,
                "force_55_70_lhk_flexory": 150
            }
        }
    }
    result_6 = _calculate_sedmy_text_podminka(measurement_data_6, results_data_6)
    print(f"   Součet: 150+150+150+150 = 600")
    print(f"   Limit: (480/2)+360 = 600")
    print(f"   600 = 600 (≤) → Výsledek:")
    print(f"   '{result_6}'")
    assert result_6 == EXPECTED_NEPREKRACUJE, f"Expected '{EXPECTED_NEPREKRACUJE}', got '{result_6}'"
    print("   ✓ PASS")

    # TEST 7: Missing work_duration → fallback na "nepřekračuje"
    print("\n[TEST 7] Chybějící work_duration → fallback 'nepřekračuje'")
    measurement_data_7 = {
        "section4_worker_a": {}
    }
    results_data_7 = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 200,
                "force_55_70_phk_flexory": 200,
                "force_55_70_lhk_extenzory": 200,
                "force_55_70_lhk_flexory": 200
            }
        }
    }
    result_7 = _calculate_sedmy_text_podminka(measurement_data_7, results_data_7)
    print(f"   work_duration chybí → Výsledek:")
    print(f"   '{result_7}'")
    assert result_7 == EXPECTED_NEPREKRACUJE, f"Expected '{EXPECTED_NEPREKRACUJE}', got '{result_7}'"
    print("   ✓ PASS")

    # TEST 8: Chybějící řádek 21 → fallback na "nepřekračuje"
    print("\n[TEST 8] Chybějící řádek 21 v tabulce → fallback 'nepřekračuje'")
    measurement_data_8 = {
        "section4_worker_a": {
            "work_duration": 480
        }
    }
    results_data_8 = {
        "table_force_distribution": {}
    }
    result_8 = _calculate_sedmy_text_podminka(measurement_data_8, results_data_8)
    print(f"   Řádek 21 chybí → Výsledek:")
    print(f"   '{result_8}'")
    assert result_8 == EXPECTED_NEPREKRACUJE, f"Expected '{EXPECTED_NEPREKRACUJE}', got '{result_8}'"
    print("   ✓ PASS")

    print("\n" + "=" * 80)
    print("✅ VŠECHNY TESTY PROŠLY!")
    print("🎯 Sedmá podmínka nyní vrací celé věty")
    print("=" * 80)


if __name__ == "__main__":
    test_sedmy_text_podminka()
