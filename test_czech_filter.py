"""
Test skript pro novou univerzální funkci format_czech_number()

Testuje všechny scénáře:
- Malá celá čísla (< 1000)
- Velká celá čísla (>= 1000)
- Malá desetinná čísla (< 1000)
- Velká desetinná čísla (>= 1000)
- Záporná čísla
- Speciální případy (None, 0, atd.)
"""
import sys
sys.path.insert(0, '.')

from generate_word_from_two_sources import format_czech_number


def test_case(value, expected, description):
    """Otestuje jeden případ a vypíše výsledek"""
    result = format_czech_number(value)
    status = "✓" if result == expected else "✗"
    print(f"{status} {description}")
    print(f"  Vstup:    {value} ({type(value).__name__})")
    print(f"  Očekáváno: {expected}")
    print(f"  Výsledek:  {result}")
    if result != expected:
        print(f"  ❌ CHYBA!")
    print()
    return result == expected


def main():
    print("=" * 80)
    print("TEST: format_czech_number() - Univerzální české formátování čísel")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    # ========== MALÁ CELÁ ČÍSLA (< 1000) ==========
    print("--- MALÁ CELÁ ČÍSLA (< 1000) ---")
    if test_case(5, "5", "Jednociferné číslo"):
        passed += 1
    else:
        failed += 1

    if test_case(150, "150", "Třímístné číslo"):
        passed += 1
    else:
        failed += 1

    if test_case(450, "450", "Běžný počet pohybů"):
        passed += 1
    else:
        failed += 1

    if test_case(999, "999", "Maximální číslo bez mezer"):
        passed += 1
    else:
        failed += 1

    # ========== VELKÁ CELÁ ČÍSLA (>= 1000) ==========
    print("--- VELKÁ CELÁ ČÍSLA (>= 1000) ---")
    if test_case(1000, "1 000", "Tisíc"):
        passed += 1
    else:
        failed += 1

    if test_case(2222, "2 222", "Čtyřmístné číslo"):
        passed += 1
    else:
        failed += 1

    if test_case(33333, "33 333", "Pětimístné číslo"):
        passed += 1
    else:
        failed += 1

    if test_case(444444, "444 444", "Šestimístné číslo"):
        passed += 1
    else:
        failed += 1

    if test_case(1234567, "1 234 567", "Sedmimístné číslo"):
        passed += 1
    else:
        failed += 1

    if test_case(123456789, "123 456 789", "Devítimístné číslo"):
        passed += 1
    else:
        failed += 1

    # ========== MALÁ DESETINNÁ ČÍSLA (< 1000) ==========
    print("--- MALÁ DESETINNÁ ČÍSLA (< 1000) ---")
    if test_case(5.5, "5,5", "Jednociferné desetinné"):
        passed += 1
    else:
        failed += 1

    if test_case(8.55, "8,6", "Zaokrouhlení nahoru"):
        passed += 1
    else:
        failed += 1

    if test_case(8.54, "8,5", "Zaokrouhlení dolů"):
        passed += 1
    else:
        failed += 1

    if test_case(11.899999, "11,9", "Float nepřesnost"):
        passed += 1
    else:
        failed += 1

    if test_case(7.2, "7,2", "Fmax hodnota"):
        passed += 1
    else:
        failed += 1

    if test_case(150.7, "150,7", "Třímístné s desetinnou"):
        passed += 1
    else:
        failed += 1

    # ========== VELKÁ DESETINNÁ ČÍSLA (>= 1000) ==========
    print("--- VELKÁ DESETINNÁ ČÍSLA (>= 1000) ---")
    if test_case(1234.5, "1 234,5", "Čtyřmístné s desetinnou"):
        passed += 1
    else:
        failed += 1

    if test_case(12345.67, "12 345,7", "Pětimístné s desetinnou + zaokrouhlení"):
        passed += 1
    else:
        failed += 1

    if test_case(123456.789, "123 456,8", "Šestimístné s desetinnou + zaokrouhlení"):
        passed += 1
    else:
        failed += 1

    if test_case(1234567.123, "1 234 567,1", "Sedmimístné s desetinnou"):
        passed += 1
    else:
        failed += 1

    # ========== SPECIÁLNÍ PŘÍPADY ==========
    print("--- SPECIÁLNÍ PŘÍPADY ---")
    if test_case(0, "0", "Nula"):
        passed += 1
    else:
        failed += 1

    if test_case(0.0, "0", "Nula float"):
        passed += 1
    else:
        failed += 1

    if test_case(None, "", "None hodnota"):
        passed += 1
    else:
        failed += 1

    if test_case("", "", "Prázdný string"):
        passed += 1
    else:
        failed += 1

    # ========== ZÁPORNÁ ČÍSLA ==========
    print("--- ZÁPORNÁ ČÍSLA ---")
    if test_case(-5, "-5", "Záporné jednociferné"):
        passed += 1
    else:
        failed += 1

    if test_case(-150, "-150", "Záporné třímístné"):
        passed += 1
    else:
        failed += 1

    if test_case(-2222, "-2 222", "Záporné s mezerami"):
        passed += 1
    else:
        failed += 1

    if test_case(-8.5, "-8,5", "Záporné desetinné"):
        passed += 1
    else:
        failed += 1

    if test_case(-12345.67, "-12 345,7", "Záporné velké desetinné"):
        passed += 1
    else:
        failed += 1

    # ========== EDGE CASES - DETEKCE CELÝCH ČÍSEL ==========
    print("--- EDGE CASES - DETEKCE CELÝCH ČÍSEL ---")
    if test_case(5.0, "5", "Float ale celé číslo (5.0 → 5)"):
        passed += 1
    else:
        failed += 1

    if test_case(1000.0, "1 000", "Float ale celé číslo s mezerami (1000.0 → 1 000)"):
        passed += 1
    else:
        failed += 1

    if test_case(450.0000001, "450", "Float nepřesnost, prakticky celé (450.0000001 → 450)"):
        passed += 1
    else:
        failed += 1

    # ========== STRING VSTUPY ==========
    print("--- STRING VSTUPY ---")
    if test_case("8.55", "8,6", "String s desetinnou"):
        passed += 1
    else:
        failed += 1

    if test_case("2222", "2 222", "String celé číslo"):
        passed += 1
    else:
        failed += 1

    # ========== VÝSLEDKY ==========
    print("=" * 80)
    print("VÝSLEDKY:")
    print("=" * 80)
    print(f"✓ Úspěšné: {passed}")
    print(f"✗ Neúspěšné: {failed}")
    print(f"Celkem: {passed + failed}")
    print()

    if failed == 0:
        print("🎉 VŠECHNY TESTY PROŠLY!")
        return 0
    else:
        print(f"⚠ {failed} testů selhalo!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
