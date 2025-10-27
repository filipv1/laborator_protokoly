"""
Test pro osmy_text_podminka - seznam činností s force_over_70 > 100

Logika:
- Pokud sesty_text_podminka = "není" → prázdný string
- Pokud sesty_text_podminka = "je":
  - Projdi všechny řádky kromě "21" (Celkem)
  - Najdi činnosti kde jakákoliv force_over_70 hodnota > 100
  - Vrať seznam oddělený čárkami
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from core.text_generator import _calculate_osmy_text_podminka


def test_osmy_text_podminka():
    """Test osmé podmínky - seznam činností"""

    print("=" * 80)
    print("TEST: osmy_text_podminka - Seznam činností s force_over_70 > 100")
    print("=" * 80)

    # TEST 1: Sesty = "není" (žádná hodnota > 100) → prázdný string
    print("\n[TEST 1] Sesty='není' → prázdný string")
    results_data_1 = {
        "table_force_distribution": {
            "1": {
                "activity": "Činnost 1",
                "force_over_70_phk_extenzory": 50,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            },
            "21": {
                "force_over_70_phk_extenzory": 50,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            }
        }
    }
    result_1 = _calculate_osmy_text_podminka(results_data_1)
    print(f"   Všechny force_over_70 < 100")
    print(f"   Výsledek: '{result_1}'")
    assert result_1 == "", f"Expected empty string, got '{result_1}'"
    print("   ✓ PASS - Prázdný string když sesty='není'")

    # TEST 2: Sesty = "je", jedna činnost má >100
    print("\n[TEST 2] Jedna činnost s force_over_70 > 100")
    results_data_2 = {
        "table_force_distribution": {
            "16": {
                "activity": "Zakládání",
                "force_over_70_phk_extenzory": 102,
                "force_over_70_phk_flexory": 3,
                "force_over_70_lhk_extenzory": 2,
                "force_over_70_lhk_flexory": 4
            },
            "17": {
                "activity": "Přestávka",
                "force_over_70_phk_extenzory": 50,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            },
            "21": {
                "force_over_70_phk_extenzory": 150,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            }
        }
    }
    result_2 = _calculate_osmy_text_podminka(results_data_2)
    print(f"   Řádek 16: force_over_70_phk_extenzory = 102 > 100")
    print(f"   Výsledek: '{result_2}'")
    assert result_2 == "Zakládání", f"Expected 'Zakládání', got '{result_2}'"
    print("   ✓ PASS")

    # TEST 3: Dvě činnosti s >100 (tvůj příklad)
    print("\n[TEST 3] Dvě činnosti s force_over_70 > 100 (reálný příklad)")
    results_data_3 = {
        "table_force_distribution": {
            "16": {
                "activity": "Zakládání",
                "force_55_70_phk_extenzory": 4,
                "force_55_70_phk_flexory": 4,
                "force_55_70_lhk_extenzory": 3,
                "force_55_70_lhk_flexory": 3,
                "force_over_70_phk_extenzory": 102,
                "force_over_70_phk_flexory": 3,
                "force_over_70_lhk_extenzory": 2,
                "force_over_70_lhk_flexory": 4
            },
            "17": {
                "activity": "Bezpečnostní přestávka",
                "force_55_70_phk_extenzory": 0,
                "force_55_70_phk_flexory": 0,
                "force_55_70_lhk_extenzory": 2,
                "force_55_70_lhk_flexory": 2,
                "force_over_70_phk_extenzory": 152,
                "force_over_70_phk_flexory": 2,
                "force_over_70_lhk_extenzory": 2,
                "force_over_70_lhk_flexory": 0
            },
            "18": {
                "activity": "Přestávka na jídlo a oddech",
                "force_55_70_phk_extenzory": 0,
                "force_55_70_phk_flexory": 0,
                "force_55_70_lhk_extenzory": 0,
                "force_55_70_lhk_flexory": 0,
                "force_over_70_phk_extenzory": 0,
                "force_over_70_phk_flexory": 0,
                "force_over_70_lhk_extenzory": 0,
                "force_over_70_lhk_flexory": 0
            },
            "21": {
                "force_over_70_phk_extenzory": 150,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            }
        }
    }
    result_3 = _calculate_osmy_text_podminka(results_data_3)
    print(f"   Řádek 16: Zakládání (102 > 100)")
    print(f"   Řádek 17: Bezpečnostní přestávka (152 > 100)")
    print(f"   Řádek 18: Přestávka na jídlo (všechny 0)")
    print(f"   Výsledek: '{result_3}'")
    assert result_3 == "Zakládání, Bezpečnostní přestávka", f"Expected 'Zakládání, Bezpečnostní přestávka', got '{result_3}'"
    print("   ✓ PASS - Přesně jak jsi chtěl!")

    # TEST 4: Sesty="je" ale žádná konkrétní činnost nemá >100 (jen Celkem)
    print("\n[TEST 4] Sesty='je' ale žádná konkrétní činnost >100")
    results_data_4 = {
        "table_force_distribution": {
            "1": {
                "activity": "Činnost 1",
                "force_over_70_phk_extenzory": 90,
                "force_over_70_phk_flexory": 80,
                "force_over_70_lhk_extenzory": 70,
                "force_over_70_lhk_flexory": 60
            },
            "2": {
                "activity": "Činnost 2",
                "force_over_70_phk_extenzory": 85,
                "force_over_70_phk_flexory": 75,
                "force_over_70_lhk_extenzory": 65,
                "force_over_70_lhk_flexory": 55
            },
            "21": {
                "force_over_70_phk_extenzory": 150,  # Jen Celkem > 100
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            }
        }
    }
    result_4 = _calculate_osmy_text_podminka(results_data_4)
    print(f"   Řádek 21: 150 > 100 (sesty='je')")
    print(f"   Ale řádky 1,2: všechny < 100")
    print(f"   Výsledek: '{result_4}'")
    assert result_4 == "", f"Expected empty string, got '{result_4}'"
    print("   ✓ PASS - Prázdný string když jen Celkem > 100")

    # TEST 5: Více činností (4)
    print("\n[TEST 5] Čtyři činnosti s force_over_70 > 100")
    results_data_5 = {
        "table_force_distribution": {
            "1": {"activity": "Činnost A", "force_over_70_phk_extenzory": 105},
            "2": {"activity": "Činnost B", "force_over_70_phk_flexory": 110},
            "3": {"activity": "Činnost C", "force_over_70_lhk_extenzory": 120},
            "4": {"activity": "Činnost D", "force_over_70_lhk_flexory": 130},
            "5": {"activity": "Činnost E", "force_over_70_phk_extenzory": 50},
            "21": {"force_over_70_phk_extenzory": 150}
        }
    }
    result_5 = _calculate_osmy_text_podminka(results_data_5)
    print(f"   Činnosti A,B,C,D: všechny > 100")
    print(f"   Činnost E: 50 < 100")
    print(f"   Výsledek: '{result_5}'")
    assert result_5 == "Činnost A, Činnost B, Činnost C, Činnost D", f"Expected 4 activities, got '{result_5}'"
    print("   ✓ PASS")

    # TEST 6: Hraničný případ - hodnota přesně 100 (nemá být zahrnuta)
    print("\n[TEST 6] Hraničný případ: force_over_70 = 100")
    results_data_6 = {
        "table_force_distribution": {
            "1": {
                "activity": "Činnost 1",
                "force_over_70_phk_extenzory": 100,
                "force_over_70_phk_flexory": 100,
                "force_over_70_lhk_extenzory": 100,
                "force_over_70_lhk_flexory": 100
            },
            "2": {
                "activity": "Činnost 2",
                "force_over_70_phk_extenzory": 101,
                "force_over_70_phk_flexory": 50,
                "force_over_70_lhk_extenzory": 50,
                "force_over_70_lhk_flexory": 50
            },
            "21": {"force_over_70_phk_extenzory": 150}
        }
    }
    result_6 = _calculate_osmy_text_podminka(results_data_6)
    print(f"   Činnost 1: všechny = 100 (ne větší)")
    print(f"   Činnost 2: 101 > 100")
    print(f"   Výsledek: '{result_6}'")
    assert result_6 == "Činnost 2", f"Expected 'Činnost 2', got '{result_6}'"
    print("   ✓ PASS - Hodnota 100 není zahrnuta")

    # TEST 7: Chybějící activity → ignorovat
    print("\n[TEST 7] Řádek bez activity → ignorovat")
    results_data_7 = {
        "table_force_distribution": {
            "1": {
                # Chybí activity!
                "force_over_70_phk_extenzory": 150
            },
            "2": {
                "activity": "Činnost 2",
                "force_over_70_phk_extenzory": 120
            },
            "21": {"force_over_70_phk_extenzory": 150}
        }
    }
    result_7 = _calculate_osmy_text_podminka(results_data_7)
    print(f"   Řádek 1: chybí activity (ignoruje se)")
    print(f"   Řádek 2: Činnost 2 (120 > 100)")
    print(f"   Výsledek: '{result_7}'")
    assert result_7 == "Činnost 2", f"Expected 'Činnost 2', got '{result_7}'"
    print("   ✓ PASS")

    print("\n" + "=" * 80)
    print("✅ VŠECHNY TESTY PROŠLY!")
    print("🎯 Osmá podmínka funguje správně")
    print("=" * 80)


if __name__ == "__main__":
    test_osmy_text_podminka()
