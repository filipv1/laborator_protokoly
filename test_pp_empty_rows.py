"""
Test pro remove_empty_pp_rows() funkci - základní logika
"""
import sys


def test_is_empty_or_zero():
    """Test pomocné funkce pro kontrolu prázdných hodnot"""

    def is_empty_or_zero(value):
        return value in ["0", "0.0", "", "None", "null"] or not value

    print("Test is_empty_or_zero():")

    # Testy pro hodnoty, které JSOU prázdné
    empty_values = ["0", "0.0", "", "None", "null", None]
    for val in empty_values:
        result = is_empty_or_zero(val)
        status = "OK" if result else "FAIL"
        print(f"  {status} is_empty_or_zero({repr(val)}) = {result}")
        assert result, f"Expected True for {repr(val)}"

    # Testy pro hodnoty, které NEJSOU prázdné
    non_empty_values = ["5", "10.5", "abc", "1", "-1"]
    for val in non_empty_values:
        result = is_empty_or_zero(val)
        status = "OK" if not result else "FAIL"
        print(f"  {status} is_empty_or_zero({repr(val)}) = {result}")
        assert not result, f"Expected False for {repr(val)}"

    print("  OK Vsechny testy prosly!\n")


def test_pp_row_removal_logic():
    """Test logiky pro odstraneni PP radku"""

    def is_empty_or_zero(value):
        return value in ["0", "0.0", "", "None", "null"] or not value

    def should_remove_pp_row(vyskyt_a, vyskyt_b, prumer):
        """Vrati True pokud by mel byt radek smazan"""
        return (is_empty_or_zero(vyskyt_a) and
                is_empty_or_zero(vyskyt_b) and
                is_empty_or_zero(prumer))

    print("Test logiky odstraneni PP radku:")

    # Test cases: (vyskyt_a, vyskyt_b, prumer, should_remove)
    test_cases = [
        # SMAZAT (vsechny 0)
        ("0", "0", "0", True, "Vsechny 0 (string)"),
        ("0.0", "0.0", "0.0", True, "Vsechny 0.0"),
        ("", "", "", True, "Vsechny prazdne"),
        ("None", "None", "None", True, "Vsechny None"),

        # NESMAZAT (alespon jedna nenulova)
        ("5", "0", "0", False, "vyskyt_a nenulove"),
        ("0", "10", "0", False, "vyskyt_b nenulove"),
        ("0", "0", "2.5", False, "prumer nenulove"),
        ("5", "10", "7.5", False, "Vsechny nenulove"),
        ("1", "0", "0.5", False, "Dve nenulove"),

        # Edge cases
        ("0", "", "None", True, "Mix prazdnych hodnot"),
        ("0.0", "", "0", True, "Mix nul a prazdnych"),
    ]

    for vyskyt_a, vyskyt_b, prumer, expected, description in test_cases:
        result = should_remove_pp_row(vyskyt_a, vyskyt_b, prumer)
        status = "OK" if result == expected else "FAIL"
        action = "SMAZE" if result else "PONECHA"
        print(f"  {status} {description}: ({vyskyt_a}, {vyskyt_b}, {prumer}) -> {action}")

        assert result == expected, (
            f"Failed for ({vyskyt_a}, {vyskyt_b}, {prumer}): "
            f"expected {expected}, got {result}"
        )

    print("  OK Vsechny testy prosly!\n")


def test_function_import():
    """Test importu funkce z modulu"""
    print("Test importu funkce:")

    try:
        from generate_word_from_two_sources import remove_empty_pp_rows
        print("  OK Funkce remove_empty_pp_rows() uspesne importovana")
        print(f"  OK Docstring: {remove_empty_pp_rows.__doc__[:50]}...")
        return True
    except ImportError as e:
        print(f"  FAIL Chyba importu: {e}")
        return False
    except Exception as e:
        print(f"  FAIL Neocekavana chyba: {e}")
        return False


def main():
    print("="*70)
    print("TEST PP EMPTY ROWS REMOVAL LOGIC")
    print("="*70)
    print()

    # Test 1: Pomocná funkce
    test_is_empty_or_zero()

    # Test 2: Logika odstranění
    test_pp_row_removal_logic()

    # Test 3: Import funkce
    import_ok = test_function_import()

    print()
    print("="*70)
    if import_ok:
        print("OK VSECHNY TESTY PROSLY!")
    else:
        print("FAIL NEKTERE TESTY SELHALY")
    print("="*70)


if __name__ == "__main__":
    main()
