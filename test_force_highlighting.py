"""
Test cerveneho zvyrazneni nadlimitnich hodnot v tabulce force_distribution
"""
import json
import sys
from pathlib import Path

# Nastav encoding pro Windows konzoli
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def test_force_highlighting():
    """Otestuj cervene zvyrazneni s realnymi daty"""

    # Najdi measurement_data.json a lsz_results.json
    measurement_path = Path("measurement_data.json")
    results_path = Path("lsz_results.json")

    if not measurement_path.exists():
        print(f"ERROR: {measurement_path} neexistuje!")
        return

    if not results_path.exists():
        print(f"ERROR: {results_path} neexistuje!")
        print("Spust nejdriv: python read_lsz_results.py")
        return

    # Nacti data
    with open(measurement_path, "r", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open(results_path, "r", encoding="utf-8") as f:
        results_data = json.load(f)

    print("=" * 80)
    print("TEST CERVENEHO ZVYRAZNENI - Tabulka force_distribution")
    print("=" * 80)
    print()

    # Vypocti hygienicky limit pro force_55_70
    work_duration = measurement_data.get("section4_worker_a", {}).get("work_duration")
    if work_duration:
        try:
            work_duration = float(work_duration)
            limit_55_70 = (work_duration / 2) + 360
        except (ValueError, TypeError):
            limit_55_70 = 600
    else:
        limit_55_70 = 600

    print("HYGIENICKY LIMIT PRO FORCE_55_70:")
    print(f"  Work duration: {work_duration} min")
    print(f"  Limit: {limit_55_70} (vzorec: (work_duration / 2) + 360)")
    print()

    # Analyzuj tabulku force_distribution
    table = results_data.get("table_force_distribution", {})
    if not table:
        print("ERROR: table_force_distribution nenalezena!")
        return

    print("ANALYZA TABULKY force_distribution:")
    print("-" * 80)

    # Statistika
    count_over_70_over_100 = 0
    count_55_70_over_limit = 0

    # Projdi vsechny radky
    for key, row in table.items():
        if key == "21":  # Skip Celkem
            continue

        activity = row.get("activity", "N/A")

        # Zkontroluj force_over_70 (konvertuj None na 0)
        force_over_70_values = [
            ("PHK ext", row.get("force_over_70_phk_extenzory") or 0),
            ("PHK flex", row.get("force_over_70_phk_flexory") or 0),
            ("LHK ext", row.get("force_over_70_lhk_extenzory") or 0),
            ("LHK flex", row.get("force_over_70_lhk_flexory") or 0)
        ]

        # Zkontroluj force_55_70 (konvertuj None na 0)
        force_55_70_values = [
            ("PHK ext", row.get("force_55_70_phk_extenzory") or 0),
            ("PHK flex", row.get("force_55_70_phk_flexory") or 0),
            ("LHK ext", row.get("force_55_70_lhk_extenzory") or 0),
            ("LHK flex", row.get("force_55_70_lhk_flexory") or 0)
        ]

        # Vypis radek pokud ma nadlimitni hodnoty
        has_over_70_over_100 = any(val > 100 for _, val in force_over_70_values)
        has_55_70_over_limit = any(val > limit_55_70 for _, val in force_55_70_values)

        if has_over_70_over_100 or has_55_70_over_limit:
            print(f"Radek {key}: {activity}")

            if has_over_70_over_100:
                print(f"  CERVENE force_over_70 (> 100):")
                for name, val in force_over_70_values:
                    if val > 100:
                        print(f"    - {name}: {val}")
                        count_over_70_over_100 += 1

            if has_55_70_over_limit:
                print(f"  CERVENE force_55_70 (> {limit_55_70}):")
                for name, val in force_55_70_values:
                    if val > limit_55_70:
                        print(f"    - {name}: {val}")
                        count_55_70_over_limit += 1

            print()

    print("-" * 80)
    print(f"CELKEM:")
    print(f"  - force_over_70 > 100: {count_over_70_over_100} hodnot bude cervene")
    print(f"  - force_55_70 > {limit_55_70}: {count_55_70_over_limit} hodnot bude cervene")
    print()

    if count_over_70_over_100 == 0 and count_55_70_over_limit == 0:
        print("ZADNE HODNOTY NEBUDOU CERVENE (vsechny pod limitem)")
    else:
        print("TYTO HODNOTY BUDOU V WORD DOKUMENTU CERVENE")

    print()
    print("=" * 80)
    print("Pro otestovani v realne Word sablone spust:")
    print("  python generate_word_from_two_sources.py")
    print("=" * 80)


if __name__ == "__main__":
    test_force_highlighting()
