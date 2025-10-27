"""
Test devate_text_podminka - tabulka hygienickych limitu
"""
import json
import sys
from pathlib import Path
from core.text_generator import generate_conditional_texts


def test_devata_podminka():
    """Test devate podminky s realnymi daty"""

    # Nastav encoding pro Windows konzoli
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

    # Nacti measurement_data.json
    measurement_path = Path("measurement_data.json")
    if not measurement_path.exists():
        print(f"ERROR: Soubor {measurement_path} neexistuje!")
        return

    with open(measurement_path, "r", encoding="utf-8") as f:
        measurement_data = json.load(f)

    # Nacti lsz_results.json
    results_path = Path("lsz_results.json")
    if not results_path.exists():
        print(f"ERROR: Soubor {results_path} neexistuje!")
        return

    with open(results_path, "r", encoding="utf-8") as f:
        results_data = json.load(f)

    # Vygeneruj podminkove texty
    texts = generate_conditional_texts(measurement_data, results_data)

    # Zobraz vysledek
    print("=" * 80)
    print("DEVATA PODMINKA - Tabulka hygienickych limitu")
    print("=" * 80)
    print()

    devata = texts.get("devata_text_podminka", {})

    if not devata:
        print("ERROR: devata_text_podminka nebyla vygeneroana!")
        return

    # Zobraz vstupni data
    print("VSTUPNI DATA:")
    print("-" * 80)
    print(f"PHK Fmax Extenzor: {results_data.get('Fmax_Phk_Extenzor')}")
    print(f"PHK Fmax Flexor: {results_data.get('Fmax_Phk_Flexor')}")
    print(f"PHK pocet pohybu: {results_data.get('phk_number_of_movements')}")
    print()
    print(f"LHK Fmax Extenzor: {results_data.get('Fmax_Lhk_Extenzor')}")
    print(f"LHK Fmax Flexor: {results_data.get('Fmax_Lhk_Flexor')}")
    print(f"LHK pocet pohybu: {results_data.get('lhk_number_of_movements')}")
    print()

    # Zobraz tabulku
    print("VYSLEDNA TABULKA:")
    print("-" * 80)
    print(f"{'PHK':<40} {'LHK':<40}")
    print(f"{'Extenzory':<20} {'Flexory':<20} {'Extenzory':<20} {'Flexory':<20}")
    print(f"{devata.get('phk_extenzory', 'N/A'):<20} {devata.get('phk_flexory', 'N/A'):<20} {devata.get('lhk_extenzory', 'N/A'):<20} {devata.get('lhk_flexory', 'N/A'):<20}")
    print()

    # Zobraz surovy dictionary
    print("SUROVY VYSTUP:")
    print("-" * 80)
    for key, value in devata.items():
        print(f"{key}: {value}")
    print()

    # Zobraz doporuceni pro Word sablonu
    print("POUZITI V WORD SABLONE:")
    print("-" * 80)
    print("V docxtpl sablone pouzijte:")
    print()
    print("{{ texts.devata_text_podminka.phk_extenzory }}")
    print("{{ texts.devata_text_podminka.phk_flexory }}")
    print("{{ texts.devata_text_podminka.lhk_extenzory }}")
    print("{{ texts.devata_text_podminka.lhk_flexory }}")
    print()
    print("Nebo v tabulce:")
    print()
    print("| PHK           | PHK           | LHK           | LHK           |")
    print("| Extenzory     | Flexory       | Extenzory     | Flexory       |")
    print("|---------------|---------------|---------------|---------------|")
    print("| {{ texts.devata_text_podminka.phk_extenzory }} | {{ texts.devata_text_podminka.phk_flexory }} | {{ texts.devata_text_podminka.lhk_extenzory }} | {{ texts.devata_text_podminka.lhk_flexory }} |")
    print()

    print("=" * 80)
    print("TEST DOKONCEN")
    print("=" * 80)


if __name__ == "__main__":
    test_devata_podminka()
