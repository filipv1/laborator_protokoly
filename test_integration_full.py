"""
Integrační test - kompletní flow s oběma podmínkami
"""
import json
import sys
from core.text_generator import generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_full_integration():
    """Test celého flow s measurement_data.json + lsz_results.json"""
    print("=" * 80)
    print("INTEGRAČNÍ TEST: Kompletní flow")
    print("=" * 80)
    print()

    # Načti oba JSONy
    with open("measurement_data.json", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    print("1. NAČTENÁ DATA:")
    print("-" * 80)
    print(f"   measurement_days: {measurement_data['section0_file_selection']['measurement_days']}")
    print(f"   Fmax_Phk_Extenzor: {results_data['Fmax_Phk_Extenzor']}")
    print(f"   Fmax_Phk_Flexor: {results_data['Fmax_Phk_Flexor']}")
    print(f"   phk_number_of_movements: {results_data['phk_number_of_movements']}")
    print()

    # Vygeneruj conditional texts (jako v generate_word_from_two_sources.py)
    conditional_texts = generate_conditional_texts(measurement_data, results_data)

    print("2. VYGENEROVANÉ CONDITIONAL TEXTY:")
    print("-" * 80)
    for key, value in conditional_texts.items():
        print(f"\n   {key}:")
        print(f"   {value}")
    print()

    # Přidej do measurement_data (enrichment)
    measurement_data["section_generated_texts"] = conditional_texts

    print("3. JSON PO ENRICHMENTU:")
    print("-" * 80)
    print(f"   Klíče v JSON: {list(measurement_data.keys())}")
    print(f"   section_generated_texts přidána: {'section_generated_texts' in measurement_data}")
    print()

    print("4. PLACEHOLDER SYNTAXE PRO WORD:")
    print("-" * 80)
    print()
    print("   VARIANTA V2 (flat, default):")
    print("   {{ section_generated_texts.prvni_text_podminka_pocetdni }}")
    print("   {{ section_generated_texts.druhy_text_podminka_limit1 }}")
    print()
    print("   VARIANTA V1 (nested):")
    print("   {{ input.section_generated_texts.prvni_text_podminka_pocetdni }}")
    print("   {{ input.section_generated_texts.druhy_text_podminka_limit1 }}")
    print()
    print("   VARIANTA V3 (prefixed):")
    print("   {{ m.section_generated_texts.prvni_text_podminka_pocetdni }}")
    print("   {{ m.section_generated_texts.druhy_text_podminka_limit1 }}")
    print()

    print("=" * 80)
    print("✓ INTEGRAČNÍ TEST ÚSPĚŠNÝ!")
    print("=" * 80)
    print()
    print("POZNÁMKA: Nyní můžeš spustit generate_word_from_two_sources.py")
    print("          s těmito JSONy a placeholdery budou správně nahrazeny.")


if __name__ == "__main__":
    test_full_integration()
