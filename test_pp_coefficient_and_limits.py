"""
Unit testy pro PP koeficient a kategoriální limity.

Testuje funkce:
- _calculate_pp_work_shift_coefficient()
- _calculate_pp_category_limits()
"""
import sys
from pathlib import Path

# Přidej core do sys.path pro import
sys.path.insert(0, str(Path(__file__).parent))

from core.text_generator import (
    _calculate_pp_work_shift_coefficient,
    _calculate_pp_category_limits
)


def test_coefficient_standard_shift():
    """Test: Standardni smena 480 min -> koeficient 1.0"""
    result = _calculate_pp_work_shift_coefficient(480)
    assert result == 1.0, f"Ocekavano 1.0, dostano {result}"
    print("[OK] Test standard shift (480 min)")


def test_coefficient_longer_shifts():
    """Test: Delší směny -> koeficient > 1.0"""
    test_cases = [
        (481, 1.025),   # 481-509: interval 1 -> +0.025
        (509, 1.025),   # 481-509: interval 1 -> +0.025
        (510, 1.05),    # 510-539: interval 2 -> +0.05
        (540, 1.075),   # 540-569: interval 3 -> +0.075
        (600, 1.125),   # 600-629: interval 5 -> +0.125
        (660, 1.175),   # 660-689: interval 7 -> +0.175 = 1.175
        (689, 1.175),   # 660-689: interval 7 -> +0.175 = 1.175
        (690, 1.2),     # >689: interval 8 -> +0.2, ale max cap 1.2
        (720, 1.2),     # max cap 1.2
    ]

    for work_min, expected in test_cases:
        result = _calculate_pp_work_shift_coefficient(work_min)
        assert abs(result - expected) < 0.001, f"Směna {work_min} min: očekáváno {expected}, dostáno {result}"
        print(f"[OK] Test longer shift ({work_min} min -> {expected}): OK")


def test_coefficient_shorter_shifts():
    """Test: Kratší směny -> koeficient < 1.0"""
    test_cases = [
        (479, 0.975),   # -1 min -> ceil(1/30) = 1 interval -> -0.025
        (450, 0.975),   # -30 min -> 1 interval
        (420, 0.95),    # -60 min -> 2 intervaly -> -0.05
        (390, 0.925),   # -90 min -> 3 intervaly
        (300, 0.85),    # -180 min -> 6 intervalů
        (270, 0.825),   # -210 min -> 7 intervalů
        (240, 0.8),     # -240 min -> min cap 0.8
        (200, 0.8),     # Extrémně krátká -> stále min cap 0.8
    ]

    for work_min, expected in test_cases:
        result = _calculate_pp_work_shift_coefficient(work_min)
        assert abs(result - expected) < 0.001, f"Směna {work_min} min: očekáváno {expected}, dostáno {result}"
        print(f"[OK] Test shorter shift ({work_min} min -> {expected}): OK")


def test_limits_standard_coefficient():
    """Test: Limity pro koeficient 1.0 (standardní směna)"""
    result = _calculate_pp_category_limits(1.0)

    # PP limity
    assert result["pp_kat1_min"] == 0
    assert result["pp_kat1_max"] == 100
    assert result["pp_kat2_min"] == 101
    assert result["pp_kat2_max"] == 160
    assert result["pp_kat3_min"] == 161

    # N limity
    assert result["n_kat1_min"] == 0
    assert result["n_kat1_max"] == 20
    assert result["n_kat2_min"] == 21
    assert result["n_kat2_max"] == 30
    assert result["n_kat3_min"] == 31

    print("[OK] Test limits standard coefficient (1.0): OK")
    print(f"  PP: 0-{result['pp_kat1_max']}, {result['pp_kat2_min']}-{result['pp_kat2_max']}, >{result['pp_kat3_min']}")
    print(f"  N: 0-{result['n_kat1_max']}, {result['n_kat2_min']}-{result['n_kat2_max']}, >{result['n_kat3_min']}")


def test_limits_longer_shift():
    """Test: Limity pro koeficient 1.05 (směna 510 min)"""
    result = _calculate_pp_category_limits(1.05)

    # PP limity: 100*1.05=105, 160*1.05=168
    assert result["pp_kat1_max"] == 105, f"Očekáváno 105, dostáno {result['pp_kat1_max']}"
    assert result["pp_kat2_min"] == 106
    assert result["pp_kat2_max"] == 168, f"Očekáváno 168, dostáno {result['pp_kat2_max']}"
    assert result["pp_kat3_min"] == 169

    # N limity: 20*1.05=21, 30*1.05=31.5->32 (round)
    assert result["n_kat1_max"] == 21
    assert result["n_kat2_min"] == 22
    assert result["n_kat2_max"] == 32  # 31.5 zaokrouhleno na 32
    assert result["n_kat3_min"] == 33

    print("[OK] Test limits longer shift (1.05): OK")
    print(f"  PP: 0-{result['pp_kat1_max']}, {result['pp_kat2_min']}-{result['pp_kat2_max']}, >{result['pp_kat3_min']}")
    print(f"  N: 0-{result['n_kat1_max']}, {result['n_kat2_min']}-{result['n_kat2_max']}, >{result['n_kat3_min']}")


def test_limits_shorter_shift():
    """Test: Limity pro koeficient 0.95 (směna 420 min)"""
    result = _calculate_pp_category_limits(0.95)

    # PP limity: 100*0.95=95, 160*0.95=152
    assert result["pp_kat1_max"] == 95
    assert result["pp_kat2_min"] == 96
    assert result["pp_kat2_max"] == 152
    assert result["pp_kat3_min"] == 153

    # N limity: 20*0.95=19, 30*0.95=28.5->29 (math round)
    assert result["n_kat1_max"] == 19
    assert result["n_kat2_min"] == 20
    assert result["n_kat2_max"] == 29  # 28.5 zaokrouhleno na 29 (_math_round)
    assert result["n_kat3_min"] == 30

    print("[OK] Test limits shorter shift (0.95): OK")
    print(f"  PP: 0-{result['pp_kat1_max']}, {result['pp_kat2_min']}-{result['pp_kat2_max']}, >{result['pp_kat3_min']}")
    print(f"  N: 0-{result['n_kat1_max']}, {result['n_kat2_min']}-{result['n_kat2_max']}, >{result['n_kat3_min']}")


def test_limits_max_coefficient():
    """Test: Limity pro max koeficient 1.2 (směna >689 min)"""
    result = _calculate_pp_category_limits(1.2)

    # PP limity: 100*1.2=120, 160*1.2=192
    assert result["pp_kat1_max"] == 120
    assert result["pp_kat2_max"] == 192

    # N limity: 20*1.2=24, 30*1.2=36
    assert result["n_kat1_max"] == 24
    assert result["n_kat2_max"] == 36

    print("[OK] Test limits max coefficient (1.2): OK")
    print(f"  PP: 0-{result['pp_kat1_max']}, {result['pp_kat2_min']}-{result['pp_kat2_max']}, >{result['pp_kat3_min']}")
    print(f"  N: 0-{result['n_kat1_max']}, {result['n_kat2_min']}-{result['n_kat2_max']}, >{result['n_kat3_min']}")


def test_limits_min_coefficient():
    """Test: Limity pro min koeficient 0.8 (směna <270 min)"""
    result = _calculate_pp_category_limits(0.8)

    # PP limity: 100*0.8=80, 160*0.8=128
    assert result["pp_kat1_max"] == 80
    assert result["pp_kat2_max"] == 128

    # N limity: 20*0.8=16, 30*0.8=24
    assert result["n_kat1_max"] == 16
    assert result["n_kat2_max"] == 24

    print("[OK] Test limits min coefficient (0.8): OK")
    print(f"  PP: 0-{result['pp_kat1_max']}, {result['pp_kat2_min']}-{result['pp_kat2_max']}, >{result['pp_kat3_min']}")
    print(f"  N: 0-{result['n_kat1_max']}, {result['n_kat2_min']}-{result['n_kat2_max']}, >{result['n_kat3_min']}")


def test_rounding_edge_cases():
    """Test: Zaokrouhlení edge cases (0.5)"""
    # Test koeficient 1.025 -> 100*1.025 = 102.5
    result = _calculate_pp_category_limits(1.025)
    assert result["pp_kat1_max"] == 102  # 102.5 -> 102 (math.floor(102.5+0.5) = 102)

    # Test koeficient 1.05 -> 20*1.05 = 21.0 (celé číslo)
    assert result["n_kat1_max"] == 21

    print("[OK] Test rounding edge cases: OK")
    print(f"  102.5 -> {result['pp_kat1_max']}")
    print(f"  21.0 -> {result['n_kat1_max']}")


def run_all_tests():
    """Spustí všechny testy"""
    print("="*60)
    print("UNIT TESTY: PP Koeficient a kategoriální limity")
    print("="*60)
    print()

    try:
        # Testy koeficientu
        print("[TESTY KOEFICIENTU]")
        test_coefficient_standard_shift()
        test_coefficient_longer_shifts()
        test_coefficient_shorter_shifts()
        print()

        # Testy limitů
        print("[TESTY LIMITU]")
        test_limits_standard_coefficient()
        test_limits_longer_shift()
        test_limits_shorter_shift()
        test_limits_max_coefficient()
        test_limits_min_coefficient()
        test_rounding_edge_cases()
        print()

        print("="*60)
        print("[OK] VSECHNY TESTY PROSLY!")
        print("="*60)

    except AssertionError as e:
        print()
        print("="*60)
        print(f"[ERROR] TEST SELHAL: {e}")
        print("="*60)
        raise


if __name__ == "__main__":
    run_all_tests()
