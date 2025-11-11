"""
Test detekce single-worker protokolu
"""
from core.text_generator import _is_single_worker_protocol

def test_single_worker_detection():
    print("=== TEST: Detekce single-worker protokolu ===\n")

    # Test 1: Prázdné full_name → single worker
    data1 = {
        "section5_worker_b": {
            "full_name": "",
            "age_years": 0
        }
    }
    result1 = _is_single_worker_protocol(data1)
    assert result1 == True, f"Test 1 FAILED: Ocekavano True, dostano {result1}"
    print("[OK] Test 1: Prazdne full_name -> single worker (True)")

    # Test 2: Vyplnene full_name -> two workers
    data2 = {
        "section5_worker_b": {
            "full_name": "Jan Novak",
            "age_years": 35
        }
    }
    result2 = _is_single_worker_protocol(data2)
    assert result2 == False, f"Test 2 FAILED: Ocekavano False, dostano {result2}"
    print("[OK] Test 2: Vyplnene full_name -> two workers (False)")

    # Test 3: Whitespace full_name -> single worker
    data3 = {
        "section5_worker_b": {
            "full_name": "   ",
            "age_years": 0
        }
    }
    result3 = _is_single_worker_protocol(data3)
    assert result3 == True, f"Test 3 FAILED: Ocekavano True, dostano {result3}"
    print("[OK] Test 3: Whitespace full_name -> single worker (True)")

    # Test 4: Chybejici section5_worker_b -> single worker (fallback)
    data4 = {}
    result4 = _is_single_worker_protocol(data4)
    assert result4 == True, f"Test 4 FAILED: Ocekavano True, dostano {result4}"
    print("[OK] Test 4: Chybejici section -> single worker (True, fallback)")

    # Test 5: None jako full_name -> single worker
    data5 = {
        "section5_worker_b": {
            "full_name": None,
            "age_years": 0
        }
    }
    result5 = _is_single_worker_protocol(data5)
    assert result5 == True, f"Test 5 FAILED: Ocekavano True, dostano {result5}"
    print("[OK] Test 5: None jako full_name -> single worker (True)")

    print("\n[SUCCESS] Vsechny testy detekce prosly!")

if __name__ == "__main__":
    test_single_worker_detection()
