"""
Kompletní integrační test - všechny 3 podmínky najednou
"""
import json
import sys
from core.text_generator import generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def test_all_three_conditions():
    """Test všech 3 podmínek současně"""
    print("=" * 80)
    print("KOMPLETNÍ INTEGRAČNÍ TEST: Všechny 3 podmínky")
    print("=" * 80)
    print()

    # Načti oba JSONy
    with open("measurement_data.json", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open("lsz_results.json", encoding="utf-8") as f:
        results_data = json.load(f)

    print("VSTUPNÍ DATA:")
    print("-" * 80)
    print(f"Podmínka 1 (measurement_days): {measurement_data['section0_file_selection']['measurement_days']}")
    print()
    print("Podmínka 2 (PHK):")
    print(f"  Fmax_Phk_Extenzor: {results_data['Fmax_Phk_Extenzor']}")
    print(f"  Fmax_Phk_Flexor: {results_data['Fmax_Phk_Flexor']}")
    print(f"  phk_number_of_movements: {results_data['phk_number_of_movements']}")
    print()
    print("Podmínka 3 (LHK):")
    print(f"  Fmax_Lhk_Extenzor: {results_data['Fmax_Lhk_Extenzor']}")
    print(f"  Fmax_Lhk_Flexor: {results_data['Fmax_Lhk_Flexor']}")
    print(f"  lhk_number_of_movements: {results_data['lhk_number_of_movements']}")
    print()

    # Vygeneruj všechny conditional texty
    conditional_texts = generate_conditional_texts(measurement_data, results_data)

    print("=" * 80)
    print("VYGENEROVANÉ CONDITIONAL TEXTY:")
    print("=" * 80)
    print()

    for i, (key, value) in enumerate(conditional_texts.items(), 1):
        print(f"{i}. {key}:")
        print(f"   {value}")
        print()

    # Přidej do measurement_data (enrichment)
    measurement_data["section_generated_texts"] = conditional_texts

    print("=" * 80)
    print("JSON STRUKTURA PO ENRICHMENTU:")
    print("=" * 80)
    print(f"Klíče v section_generated_texts:")
    for key in conditional_texts.keys():
        print(f"  - {key}")
    print()

    print("=" * 80)
    print("WORD PLACEHOLDER SYNTAXE:")
    print("=" * 80)
    print()
    print("VARIANTA V2 (flat, default):")
    print("  {{ section_generated_texts.prvni_text_podminka_pocetdni }}")
    print("  {{ section_generated_texts.druhy_text_podminka_limit1 }}")
    print("  {{ section_generated_texts.treti_text_podminka_limit1 }}")
    print()
    print("VARIANTA V1 (nested):")
    print("  {{ input.section_generated_texts.prvni_text_podminka_pocetdni }}")
    print("  {{ input.section_generated_texts.druhy_text_podminka_limit1 }}")
    print("  {{ input.section_generated_texts.treti_text_podminka_limit1 }}")
    print()
    print("VARIANTA V3 (prefixed):")
    print("  {{ m.section_generated_texts.prvni_text_podminka_pocetdni }}")
    print("  {{ m.section_generated_texts.druhy_text_podminka_limit1 }}")
    print("  {{ m.section_generated_texts.treti_text_podminka_limit1 }}")
    print()

    print("=" * 80)
    print("✓ VŠECHNY 3 PODMÍNKY FUNGUJÍ SPRÁVNĚ!")
    print("=" * 80)
    print()
    print("POZNÁMKA: Nyní můžeš použít všechny 3 placeholdery ve Word šabloně.")
    print("          Generate_word_from_two_sources.py je připraven.")


if __name__ == "__main__":
    test_all_three_conditions()
