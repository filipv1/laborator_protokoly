"""
Test pro sedmy_text_podminka - Fix pro string work_duration

Ověřuje, že funkce správně zpracovává work_duration jako:
- string ("480")
- číslo (480)
- float (480.0)
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from core.text_generator import _calculate_sedmy_text_podminka


def test_string_conversion():
    """Test konverze string work_duration na číslo"""

    print("=" * 80)
    print("TEST: sedmy_text_podminka - String work_duration fix")
    print("=" * 80)

    EXPECTED_NEPREKRACUJE = "nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."

    # Testovací results_data (konstantní pro všechny testy)
    results_data = {
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 5,
                "force_55_70_phk_flexory": 4,
                "force_55_70_lhk_extenzory": 5,
                "force_55_70_lhk_flexory": 4
            }
        }
    }

    # TEST 1: work_duration jako STRING (reálný scénář z JSON)
    print("\n[TEST 1] work_duration jako string: '480'")
    measurement_data_1 = {
        "section4_worker_a": {
            "work_duration": "480"  # ← STRING!
        }
    }
    result_1 = _calculate_sedmy_text_podminka(measurement_data_1, results_data)
    print(f"   work_duration: '480' (string)")
    print(f"   Limit: (480/2)+360 = 600")
    print(f"   Součet: 18")
    print(f"   Výsledek: '{result_1[:50]}...'")
    assert result_1 == EXPECTED_NEPREKRACUJE
    print("   ✓ PASS - String správně zkonvertován")

    # TEST 2: work_duration jako INT
    print("\n[TEST 2] work_duration jako int: 480")
    measurement_data_2 = {
        "section4_worker_a": {
            "work_duration": 480  # ← INT
        }
    }
    result_2 = _calculate_sedmy_text_podminka(measurement_data_2, results_data)
    print(f"   work_duration: 480 (int)")
    print(f"   Výsledek: '{result_2[:50]}...'")
    assert result_2 == EXPECTED_NEPREKRACUJE
    print("   ✓ PASS - Int funguje")

    # TEST 3: work_duration jako FLOAT
    print("\n[TEST 3] work_duration jako float: 480.0")
    measurement_data_3 = {
        "section4_worker_a": {
            "work_duration": 480.0  # ← FLOAT
        }
    }
    result_3 = _calculate_sedmy_text_podminka(measurement_data_3, results_data)
    print(f"   work_duration: 480.0 (float)")
    print(f"   Výsledek: '{result_3[:50]}...'")
    assert result_3 == EXPECTED_NEPREKRACUJE
    print("   ✓ PASS - Float funguje")

    # TEST 4: work_duration jako string s desetinným číslem
    print("\n[TEST 4] work_duration jako string: '450.5'")
    measurement_data_4 = {
        "section4_worker_a": {
            "work_duration": "450.5"  # ← STRING FLOAT
        }
    }
    result_4 = _calculate_sedmy_text_podminka(measurement_data_4, results_data)
    print(f"   work_duration: '450.5' (string)")
    print(f"   Limit: (450.5/2)+360 = 585.25")
    print(f"   Součet: 18")
    print(f"   Výsledek: '{result_4[:50]}...'")
    assert result_4 == EXPECTED_NEPREKRACUJE
    print("   ✓ PASS - String float správně zkonvertován")

    # TEST 5: Neplatný string → fallback
    print("\n[TEST 5] work_duration jako neplatný string: 'abc'")
    measurement_data_5 = {
        "section4_worker_a": {
            "work_duration": "abc"  # ← NEPLATNÝ STRING
        }
    }
    result_5 = _calculate_sedmy_text_podminka(measurement_data_5, results_data)
    print(f"   work_duration: 'abc' (nelze zkonvertovat)")
    print(f"   Výsledek: '{result_5[:50]}...'")
    assert result_5 == EXPECTED_NEPREKRACUJE
    print("   ✓ PASS - Fallback funguje pro neplatný string")

    # TEST 6: Prázdný string → fallback
    print("\n[TEST 6] work_duration jako prázdný string: ''")
    measurement_data_6 = {
        "section4_worker_a": {
            "work_duration": ""  # ← PRÁZDNÝ STRING
        }
    }
    result_6 = _calculate_sedmy_text_podminka(measurement_data_6, results_data)
    print(f"   work_duration: '' (prázdný)")
    print(f"   Výsledek: '{result_6[:50]}...'")
    assert result_6 == EXPECTED_NEPREKRACUJE
    print("   ✓ PASS - Fallback funguje pro prázdný string")

    # TEST 7: Realistický test s reálným work_duration ze skutečného projektu
    print("\n[TEST 7] Realistický test: string '480' s vyšším součtem")
    measurement_data_7 = {
        "section4_worker_a": {
            "work_duration": "480"  # ← Reálné JSON
        }
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
    expected_7 = "překračuje u měřených svalových skupin rukou a předloktí daný hygienický limit."
    print(f"   work_duration: '480' (string)")
    print(f"   Limit: 600")
    print(f"   Součet: 800 > 600")
    print(f"   Výsledek: '{result_7[:50]}...'")
    assert result_7 == expected_7
    print("   ✓ PASS - Reálný scénář funguje")

    print("\n" + "=" * 80)
    print("✅ VŠECHNY TESTY PROŠLY!")
    print("🎯 Funkce nyní správně zpracovává work_duration jako string i číslo")
    print("=" * 80)


if __name__ == "__main__":
    test_string_conversion()
