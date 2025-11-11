"""
Test vypoctu Q8 = work_duration - breaks v PP Excelech
"""
from core.excel_filler import ExcelFiller

def test_q8_calculation():
    print("=== TEST: Q8 vypocet (work_duration - breaks) ===\n")

    # Testovaci mapping
    test_mapping = {
        "Test": {
            "Q8": "CALC:section4_worker_a.work_duration-section4_worker_a.breaks"
        }
    }

    # Testovaci data
    test_data = {
        "section4_worker_a": {
            "work_duration": 480,
            "breaks": 30
        }
    }

    # Vytvor ExcelFiller
    filler = ExcelFiller(test_mapping)

    # Test vypoctu
    result = filler._get_value_from_json(test_data, "CALC:section4_worker_a.work_duration-section4_worker_a.breaks")

    print(f"work_duration: {test_data['section4_worker_a']['work_duration']}")
    print(f"breaks: {test_data['section4_worker_a']['breaks']}")
    print(f"Vypocteno Q8: {result}")
    print(f"Ocekavano: 450 (480 - 30)")

    assert result == 450, f"CHYBA: Ocekavano 450, dostano {result}"
    print("\n[OK] Vypocet Q8 funguje spravne!")

    # Test s roznymi hodnotami
    print("\n=== Test s jinymi hodnotami ===")
    test_data2 = {
        "section4_worker_a": {
            "work_duration": 510,
            "breaks": 45
        }
    }

    result2 = filler._get_value_from_json(test_data2, "CALC:section4_worker_a.work_duration-section4_worker_a.breaks")
    print(f"work_duration: {test_data2['section4_worker_a']['work_duration']}")
    print(f"breaks: {test_data2['section4_worker_a']['breaks']}")
    print(f"Vypocteno Q8: {result2}")
    print(f"Ocekavano: 465 (510 - 45)")

    assert result2 == 465, f"CHYBA: Ocekavano 465, dostano {result2}"
    print("\n[OK] Test s jinymi hodnotami OK!")

    # Test s nulovou prestavkou
    print("\n=== Test s nulovou prestavkou ===")
    test_data3 = {
        "section4_worker_a": {
            "work_duration": 480,
            "breaks": 0
        }
    }

    result3 = filler._get_value_from_json(test_data3, "CALC:section4_worker_a.work_duration-section4_worker_a.breaks")
    print(f"work_duration: {test_data3['section4_worker_a']['work_duration']}")
    print(f"breaks: {test_data3['section4_worker_a']['breaks']}")
    print(f"Vypocteno Q8: {result3}")
    print(f"Ocekavano: 480 (480 - 0)")

    assert result3 == 480, f"CHYBA: Ocekavano 480, dostano {result3}"
    print("\n[OK] Test s nulovou prestavkou OK!")

    print("\n[SUCCESS] Vsechny testy prosly!")

if __name__ == "__main__":
    test_q8_calculation()
