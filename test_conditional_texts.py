"""
Test skript pro ověření funkčnosti conditional texts
"""
import json
import sys
from core.text_generator import generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_conditional_texts():
    """Test generování podmínkových textů"""

    # Test 1: measurement_days = 2
    print("=" * 60)
    print("TEST 1: measurement_days = 2")
    print("=" * 60)

    test_data_2_days = {
        "section0_file_selection": {
            "measurement_days": 2
        }
    }

    result = generate_conditional_texts(test_data_2_days)
    print(f"Vygenerovaný text:")
    print(f"  {result['prvni_text_podminka_pocetdni']}")
    print()

    expected = "Měření probíhalo ve dvou dnech, ve dvou průměrných směnách. Měřeni byli 2 pracovníci – muži."
    assert result['prvni_text_podminka_pocetdni'] == expected, "Text se neshoduje!"
    print("✓ TEST 1 ÚSPĚŠNÝ")
    print()

    # Test 2: measurement_days = 1
    print("=" * 60)
    print("TEST 2: measurement_days = 1")
    print("=" * 60)

    test_data_1_day = {
        "section0_file_selection": {
            "measurement_days": 1
        }
    }

    result = generate_conditional_texts(test_data_1_day)
    print(f"Vygenerovaný text:")
    print(f"  {result['prvni_text_podminka_pocetdni']}")
    print()

    expected = "Měření probíhalo v jednom dni, v jedné průměrné směně. Měřeni byli 2 pracovníci – muži."
    assert result['prvni_text_podminka_pocetdni'] == expected, "Text se neshoduje!"
    print("✓ TEST 2 ÚSPĚŠNÝ")
    print()

    # Test 3: Test s reálnými daty z measurement_data.json
    print("=" * 60)
    print("TEST 3: Reálná data z measurement_data.json")
    print("=" * 60)

    with open("measurement_data.json", encoding="utf-8") as f:
        real_data = json.load(f)

    result = generate_conditional_texts(real_data)
    print(f"measurement_days v souboru: {real_data['section0_file_selection']['measurement_days']}")
    print(f"Vygenerovaný text:")
    print(f"  {result['prvni_text_podminka_pocetdni']}")
    print()
    print("✓ TEST 3 ÚSPĚŠNÝ")
    print()

    print("=" * 60)
    print("VŠECHNY TESTY PROŠLY!")
    print("=" * 60)


if __name__ == "__main__":
    test_conditional_texts()
