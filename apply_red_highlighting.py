"""
Aplikovat cervene zvyrazneni na EXISTUJICI Word dokument
"""
import json
import sys
from pathlib import Path
from core.text_generator import highlight_force_distribution_values

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def apply_highlighting(docx_path, measurement_json, results_json):
    """Aplikuj cervene zvyrazneni na existujici dokument"""

    # Nacti JSONy
    with open(measurement_json, 'r', encoding='utf-8') as f:
        measurement_data = json.load(f)

    with open(results_json, 'r', encoding='utf-8') as f:
        results_data = json.load(f)

    print(f"Aplikuji cervene zvyrazneni na: {docx_path}")
    print(f"Measurement data: {measurement_json}")
    print(f"Results data: {results_json}")
    print()

    # Aplikuj zvyrazneni
    highlight_force_distribution_values(str(docx_path), measurement_data, results_data)

    print("HOTOVO! Dokument byl upraven.")
    print("Otevri dokument ve Wordu a zkontroluj cervene hodnoty.")


if __name__ == "__main__":
    apply_highlighting(
        "projects/222_rentury/LSZ_protokol.docx",
        "projects/222_rentury/measurement_data.json",
        "projects/222_rentury/lsz_results.json"
    )
