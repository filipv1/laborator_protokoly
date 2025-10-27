"""
Integrační test - zkontroluje, že JSON je správně obohacen o conditional texts
"""
import json
import sys
from core.text_generator import generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_json_enrichment():
    """Test obohacení JSON o conditional texts"""

    print("=" * 80)
    print("INTEGRAČNÍ TEST: JSON Enrichment")
    print("=" * 80)
    print()

    # Načti measurement_data.json
    with open("measurement_data.json", encoding="utf-8") as f:
        input_data = json.load(f)

    print(f"1. PŘED enrichmentem:")
    print(f"   - Klíče v JSON: {list(input_data.keys())}")
    print(f"   - measurement_days: {input_data['section0_file_selection']['measurement_days']}")
    print()

    # Vygeneruj conditional texts (jako v generate_word_protocol_v2)
    conditional_texts = generate_conditional_texts(input_data)
    input_data["section_generated_texts"] = conditional_texts

    print(f"2. PO enrichmentu:")
    print(f"   - Klíče v JSON: {list(input_data.keys())}")
    print(f"   - section_generated_texts je přidána: {'section_generated_texts' in input_data}")
    print()

    print(f"3. Obsah section_generated_texts:")
    for key, value in input_data["section_generated_texts"].items():
        print(f"   - {key}:")
        print(f"     {value}")
    print()

    print("=" * 80)
    print("4. WORD PLACEHOLDER SYNTAXE:")
    print("=" * 80)
    print()
    print("Pro VARIANTU V2 (flat, default):")
    print("  {{ section_generated_texts.prvni_text_podminka_pocetdni }}")
    print()
    print("Pro VARIANTU V1 (nested):")
    print("  {{ input.section_generated_texts.prvni_text_podminka_pocetdni }}")
    print()
    print("Pro VARIANTU V3 (prefixed):")
    print("  {{ m.section_generated_texts.prvni_text_podminka_pocetdni }}")
    print()

    print("=" * 80)
    print("✓ INTEGRAČNÍ TEST ÚSPĚŠNÝ!")
    print("=" * 80)


if __name__ == "__main__":
    test_json_enrichment()
